#!/usr/bin/env python3
"""Download, verify, reassemble, and optionally extract the AoAS records.

Python 3.9+; standard library only. Run --help for options.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import urllib.request
import zipfile

BLOCK = 8 * 1024 * 1024


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(BLOCK), b''):
            h.update(block)
    return h.hexdigest()


def checked(path, spec):
    return path.is_file() and path.stat().st_size == spec['bytes'] and digest(path) == spec['sha256']


def safe_name(name):
    if not re.fullmatch(r'[A-Za-z0-9_.-]+', name) or name in ('.', '..'):
        raise ValueError('Unsafe archive or asset name: ' + repr(name))
    return name


def download(spec, directory, base_url):
    name = safe_name(spec['name'])
    target = directory / name
    if checked(target, spec):
        print('Verified existing asset:', name, flush=True)
        return target
    if target.exists():
        raise RuntimeError('Existing file failed verification; move it aside before retrying: ' + str(target))
    partial = directory / (name + '.download')
    offset = partial.stat().st_size if partial.exists() else 0
    if offset > spec['bytes']:
        raise RuntimeError('Oversized partial download: ' + str(partial))
    if offset < spec['bytes']:
        headers = {'User-Agent': 'SQS-AoAS-reproducibility/2026-09-15'}
        if offset:
            headers['Range'] = 'bytes=' + str(offset) + '-'
        request = urllib.request.Request(base_url + '/' + name, headers=headers)
        with urllib.request.urlopen(request, timeout=90) as response:
            resumed = offset and response.status == 206
            if resumed and not response.headers.get('Content-Range', '').startswith('bytes ' + str(offset) + '-'):
                raise RuntimeError('Unexpected HTTP range response for ' + name)
            mode = 'ab' if resumed else 'wb'
            downloaded = offset if resumed else 0
            reported = downloaded // (100 * 1024 * 1024)
            with partial.open(mode) as output:
                for block in iter(lambda: response.read(BLOCK), b''):
                    output.write(block)
                    downloaded += len(block)
                    if downloaded > spec['bytes']:
                        raise RuntimeError('Download exceeds the recorded size: ' + name)
                    progress = downloaded // (100 * 1024 * 1024)
                    if progress > reported:
                        print(name, str(round(downloaded / spec['bytes'] * 100, 1)) + '%', flush=True)
                        reported = progress
    if not checked(partial, spec):
        raise RuntimeError('SHA-256 or size mismatch: ' + str(partial))
    os.replace(partial, target)
    print('Downloaded and verified:', name, flush=True)
    return target


def assemble(spec, directory):
    name = safe_name(spec['name'])
    target = directory / name
    if checked(target, spec):
        print('Verified complete archive:', name, flush=True)
        return target
    if target.exists():
        raise RuntimeError('Existing archive failed verification: ' + str(target))
    parts = [directory / safe_name(p['name']) for p in spec['assets']]
    for path, part in zip(parts, spec['assets']):
        if not checked(path, part):
            raise RuntimeError('Missing or corrupt download part: ' + str(path))
    temporary = directory / (name + '.assembling')
    if temporary.exists():
        raise RuntimeError('Move aside the previous incomplete assembly before retrying: ' + str(temporary))
    h = hashlib.sha256()
    size = 0
    try:
        with temporary.open('xb') as output:
            for part in parts:
                with part.open('rb') as stream:
                    for block in iter(lambda: stream.read(BLOCK), b''):
                        output.write(block)
                        h.update(block)
                        size += len(block)
        if size != spec['bytes'] or h.hexdigest() != spec['sha256']:
            raise RuntimeError('Reconstructed archive hash differs: ' + name)
        os.replace(temporary, target)
    except BaseException:
        if temporary.exists():
            temporary.unlink()
        raise
    print('Reconstructed and verified:', name, flush=True)
    return target


def extract(archive, directory, top_directory):
    with zipfile.ZipFile(archive) as z:
        members = z.infolist()
        for info in members:
            path = PurePosixPath(info.filename)
            if '\\' in info.filename or ':' in info.filename or path.is_absolute() or '..' in path.parts or not path.parts or path.parts[0] != top_directory:
                raise RuntimeError('Unsafe ZIP path: ' + info.filename)
            if stat.S_ISLNK(info.external_attr >> 16):
                raise RuntimeError('ZIP symlinks are not supported: ' + info.filename)
            destination = directory.joinpath(*path.parts).resolve()
            if directory.resolve() not in destination.parents:
                raise RuntimeError('ZIP path leaves extraction directory: ' + info.filename)
        z.extractall(directory)
    print('Extracted:', archive.name, flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=Path(__file__).with_name('release_manifest.json'))
    parser.add_argument('--output-dir', type=Path, default=Path('aoas-records'))
    parser.add_argument('--assemble-only', action='store_true', help='Use already downloaded files; make no network requests.')
    parser.add_argument('--extract', action='store_true', help='Extract verified archives in the recorded order into a new extracted/ directory.')
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    base = manifest['download_base_url']
    if not base.startswith('https://github.com/ishspsy/SQS-AoAS/releases/download/'):
        raise ValueError('Unexpected release host or repository in manifest')
    args.output_dir.mkdir(parents=True, exist_ok=True)
    extracted = args.output_dir / 'extracted'
    if args.extract and extracted.exists():
        raise RuntimeError('Choose a new output directory or move existing extracted/ aside to protect existing analyses.')
    archives = []
    for spec in sorted(manifest['archives'], key=lambda item: item['extraction_order']):
        print('Archive:', spec['name'], flush=True)
        complete = args.output_dir / safe_name(spec['name'])
        if not args.assemble_only and not checked(complete, spec):
            for part in spec['assets']:
                download(part, args.output_dir, base)
        archives.append(assemble(spec, args.output_dir))
    if args.extract:
        extracted.mkdir()
        for archive in archives:
            extract(archive, extracted, manifest['top_directory'])
        print('Reconstruction directory:', extracted / manifest['top_directory'])
    print('All requested archives are verified. No statistical model was fitted.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, RuntimeError, zipfile.BadZipFile) as error:
        sys.exit(str(error))
