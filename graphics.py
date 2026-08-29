from dataclasses import dataclass,replace
from blocks import Block, FenceSolution
from IPython.display import SVG, display

# Класс Точка
@dataclass
class Point:
    x : float
    y : float

# Отрисовка блока - базовая единица
def DrawBlock(
        block : Block,
        xy : Point
) -> str :
    return f"""
        <rect
            x="{xy.x}"
            y="{xy.y}"
            width="{block.length_mm}"
            height="{block.height_mm}"
            fill="lightgray"
            stroke="black"
            stroke-width="5"
        />
    """

# Отрисовка колонны
def DrawColumn(
        count_blocks : int,
        block : Block,
        xy : Point
) -> str :

    svg = ""
    for bl in range(count_blocks):
        xy_block = Point(xy.x,xy.y - block.height_mm * (bl + 1))
        svg += DrawBlock(block,xy_block)
    return svg

# Отрисовка всех колонн
def DrawAllColumns(
        count_blocks : int,
        count_columns : int,
        spance_length : float,
        block : Block,
        xy : Point
) -> str :

    svg = ""
    for col in range(count_columns):
        xy_column = Point(xy.x+spance_length*col,xy.y)
        svg += DrawColumn(
            count_blocks,
            block,
            xy_column
        )
    return svg

# Отрисовка пролета
def DrawSpan(
        count_blocks_row : int,
        count_blocks_column : int,
        block : Block,
        block_cutted : Block|None,
        xy : Point
) -> str :

    svg = ""
    for column in range(count_blocks_column):
        for row in range(count_blocks_row):
            xy_block = Point(
                xy.x + block.length_mm * row,
                xy.y - block.height_mm * (column + 1),
            )
            svg += DrawBlock(block, xy_block)
        if block_cutted is not None:
            xy_cutted = Point(
                xy.x + block.length_mm * count_blocks_row,
                xy.y - block.height_mm * (column + 1),
                            )
            svg += DrawBlock(block_cutted, xy_cutted)



    return svg

# Отрисовка забора
def DrawAll(
        fence_solution : FenceSolution,
) -> str :
# определяем переменные
    count_column_blocks = fence_solution.column_blocks_per_column
    count_columns = fence_solution.columns_count
    block_column = fence_solution.column_block

    count_fence_blocks_x = fence_solution.fence_blocks_per_row_x
    count_fence_blocks_y = fence_solution.fence_blocks_per_row_y
    block_fence = fence_solution.fence_block

    spance_length = fence_solution.spans_length

    # создаем объект - блок отрезанный
    block_cutted = None


    if fence_solution.cutted_block_length > 0:
        block_cutted = replace(
            block_fence,
            length_mm=fence_solution.cutted_block_length,
        )

    xy = Point(0,
               max(
                   fence_solution.fence_params.height_fence,
                   fence_solution.fence_params.height_column
               )
               )


    svg = ""

    for col in range(count_columns):
        xy_column = Point(
            xy.x+(block_column.length_mm + spance_length)*col,
            xy.y
        )
        svg += DrawColumn(
            count_column_blocks,
            block_column,
            xy_column
        )
        if col < count_columns - 1:
            xy_fence = Point(xy_column.x+block_column.length_mm,xy_column.y)
            svg += DrawSpan(
                count_fence_blocks_x,
                count_fence_blocks_y,
                block_fence,
                block_cutted,
                xy_fence
            )
    return svg

# Показываем
def DisplaySVG(block_svg,x,y):
    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg"
         viewBox="0 0 {x} {y}">

        {block_svg}

    </svg>
    """
    display(SVG(svg))