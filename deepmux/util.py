import os

import tqdm


class ProgressReader:

    def __init__(self, filename):
        self.filename = filename
        self.total_size = os.path.getsize(filename)

    def __iter__(self):
        chunk_size = 1 << 20
        pbar = tqdm.tqdm(total=self.total_size / chunk_size,
                         unit='MB',
                         unit_scale=True,
                         unit_divisor=chunk_size)
        try:
            with open(self.filename, 'rb') as file:
                while True:
                    data = file.read(chunk_size)
                    if not data:
                        break
                    pbar.update(len(data))
                    yield data
        finally:
            pbar.close()

    def __len__(self):
        return self.total_size
