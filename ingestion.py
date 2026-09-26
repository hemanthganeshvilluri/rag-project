from pathlib import Path

def ingestion(document, converter):
    path = Path(document)
    if path.is_file():
        files = [path]
    elif path.is_dir():
        files = [file for file in path.rglob('*') if file.is_file()]
    else:
        raise FileNotFoundError(f'path not found{document}')

    results = []
    for file in files:
        try:
            result = converter.convert(file)
            results.append({
                'source': str(file),
                'document': result.document
            })
        except Exception as e:
            import traceback
            print(f'failed to process {file}: {e}')
            traceback.print_exc()
    return results
