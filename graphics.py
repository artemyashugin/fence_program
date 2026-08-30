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

# Отрисовка пролета
def DrawSpan(
        count_blocks_row : int,
        count_blocks_column : int,
        block : Block,
        block_cutted : Block|None,
        n : int|None,
        xy : Point
) -> str :
    if block_cutted is not None:
        block_cutted_length = block_cutted.length_mm
    else:
        block_cutted_length = 0
    svg = ""
    for column in range(count_blocks_column):
        y_offset = xy.y - block.height_mm * (column + 1)
        # левая подрезка
        if block_cutted is not None and n == 2:
            xy_block_cutted_2 = Point(
                xy.x,
                y_offset,
            )
            svg += DrawBlock(block_cutted, xy_block_cutted_2)
        # полные блоки
        for row in range(count_blocks_row):
            xy_block = Point(
                xy.x + block.length_mm * row + block_cutted_length*(n-1),
                y_offset,
            )
            svg += DrawBlock(block, xy_block)
        # правая подрезка
        if block_cutted is not None and (n == 1 or n == 2):
            xy_cutted_1 = Point(
                xy.x + block.length_mm * count_blocks_row + block_cutted_length*(n-1),
                y_offset,
                )
            svg += DrawBlock(block_cutted, xy_cutted_1)



    return svg

def CreateSegments(fence_solution: FenceSolution,):
    segments = []

    fence_count = fence_solution.fence_spans_count
    column_length = fence_solution.column_block.length_mm
    span_length = fence_solution.spans_length

    gates_length = (
            fence_solution.fence_params.gates_length or []
    )

    segments.append(('column',column_length))
    for span in range(fence_count):
        segments.append(('span',span_length))
        segments.append(('column',column_length))

        if span < len(gates_length):
            segments.append(("gate",gates_length[span]))
            segments.append(("column",column_length))
    return segments


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

    gates_length  = fence_solution.fence_params.gates_length

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

    segments = CreateSegments(fence_solution)

    x = xy.x
    for segment_type,segment_length in segments:
        segment_cord = Point(x,xy.y)
        if segment_type == 'column':
            svg += DrawColumn(
                count_column_blocks,
                block_column,
                segment_cord
            )

        if segment_type == 'span':
            svg += DrawSpan(
                count_fence_blocks_x,
                count_fence_blocks_y,
                block_fence,
                block_cutted,
                fence_solution.fence_blocks_per_row_x_cutted,
                segment_cord,
            )

        if segment_type == 'gate':
            pass

        x += segment_length

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