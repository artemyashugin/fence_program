from dataclasses import dataclass

import numpy as np

@dataclass
class Block:
    length_mm: float = .0
    width_mm: int = 0
    height_mm: int = 0
    mass_kg: float = .0
    price_rub: int = 0

@dataclass
class FenceParams:
    length_front : int = 0
    height_fence : int = 0
    height_column : int = 0

    columns_count : int = 0
    gates_length : list[int] = 0

    @property
    def gates(self):
        if self.gates_length == 0:
            return 0
        else:
            return len(self.gates_length)

@dataclass()
class FenceSolution:
    columns_count: int = 0                 # количество колонн
    fence_spans_count: int = 0             # количество пролетов
    spans_length: int = 0                  # длина пролета

    column_blocks_per_column: int = 0      # количество блоков в колонне

    fence_blocks_per_row_y: int = 0        # количество блоков в пролете в длину
    fence_blocks_per_row_x: int = 0        # количество блоков в пролете в высоту

    fence_blocks_per_row_x_cutted: int = 0 # количество подрезанных блоков в пролете в длину
    cutted_block_length: float = .0        # длина подрезанного блока

    fence_block: Block = None
    column_block: Block = None
    fence_params: FenceParams = None

    error : bool = False

    def count(self):

        self.column_blocks = self.column_blocks_per_column*self.columns_count
        self.fence_blocks = int(self.fence_blocks_per_row_y*self.fence_blocks_per_row_x*self.fence_spans_count)
        self.fence_blocks_cutted = self.fence_blocks_per_row_y*self.fence_blocks_per_row_x_cutted*self.fence_spans_count

    def show(self):
        self.count()
        print('Количество пролетов: ',self.fence_spans_count)
        print(f'Длина пролета: {self.spans_length} мм')
        print('Количество столбов: ',self.columns_count)
        print(f'\n')

        print('Количество столбовых блоков: ',self.column_blocks)
        print('Количество рядовых блоков: ',self.fence_blocks)
        print(f'\n')

        print('Количество рядовых блоков с подрезкой: ',self.fence_blocks_cutted)
        print(f'Длина подрезанного блока: {self.cutted_block_length} мм')

def Solution(fence_params: FenceParams,fence_block : Block,column_block : Block,n : int):
    MIN_BLOCK_LENGTH = 100

    fence_solution = FenceSolution(
        fence_block=fence_block,
        column_block=column_block,
        fence_params=fence_params
    )

    # количество колонн общее
    fence_solution.columns_count = fence_params.columns_count + fence_params.gates

    # количество пролетов
    fence_solution.fence_spans_count = fence_params.columns_count - 1

    free_length = (fence_params.length_front - np.sum(fence_params.gates_length) - fence_params.columns_count * column_block.length_mm)

    if free_length <= 0:
        print("Столбы не помещаются в заданную длину")
        fence_solution.error = True
        return None

    fence_solution.spans_length = free_length / fence_solution.fence_spans_count

    #без подрезки
    if n == 0:

        if fence_solution.spans_length % fence_block.length_mm != 0:
            print('Без подрезки не обойтись')
            fence_solution.error = True
            return fence_solution
        else:
            fence_solution.fence_blocks_per_row_x_cutted = 0
            fence_solution.cutted_block_length = 0
            fence_solution.fence_blocks_per_row_x = int(fence_solution.spans_length // fence_block.length_mm)
    # подрезка одного блока
    if n == 1:
        if fence_solution.spans_length % fence_block.length_mm != 0:
            full_blocks, remainder = divmod(fence_solution.spans_length,fence_block.length_mm,)

            if remainder < MIN_BLOCK_LENGTH:
                print(f'Длина блока для подрезки меньше {MIN_BLOCK_LENGTH} мм')
                return fence_solution

            fence_solution.fence_blocks_per_row_x = int(full_blocks)
            fence_solution.cutted_block_length = remainder
            fence_solution.fence_blocks_per_row_x_cutted = 1
        else:
            fence_solution.fence_blocks_per_row_x_cutted = 0
            fence_solution.cutted_block_length = 0
            fence_solution.fence_blocks_per_row_x = int(fence_solution.spans_length // fence_block.length_mm)

            print('Можно обойтись без подрезки')

    # подрезка двух блоков
    if n == 2:
        if fence_solution.spans_length % fence_block.length_mm != 0:
            full_blocks, remainder = divmod(fence_solution.spans_length,fence_block.length_mm,)

            if remainder < MIN_BLOCK_LENGTH:
                full_blocks -= 1
                remainder += fence_block.length_mm

            fence_solution.fence_blocks_per_row_x = int(full_blocks)
            fence_solution.cutted_block_length = remainder/2
            fence_solution.fence_blocks_per_row_x_cutted = 2
        else:
            fence_solution.fence_blocks_per_row_x_cutted = 0
            fence_solution.cutted_block_length = 0
            fence_solution.fence_blocks_per_row_x = int(fence_solution.spans_length // fence_block.length_mm)

            print('Можно обойтись без подрезки')

    # количество блоков в колонне и в пролете в высоту
    fence_solution.column_blocks_per_column = int(fence_params.height_column/column_block.height_mm)
    fence_solution.fence_blocks_per_row_y = int(fence_params.height_fence/fence_block.height_mm)

    return fence_solution