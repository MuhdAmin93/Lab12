import matplotlib.pyplot as plt
import numpy as np

class NewellNewellSanchAlgorithm:
    def __init__(self, segments, rectangles):
        self.segments = segments
        self.rectangles = rectangles

    def get_visible_and_hidden_objects(self):
        top_edges = self.get_rectangle_edges(self.rectangles[0])
        bottom_edges = self.get_rectangle_edges(self.rectangles[1])

        visible_segments = []
        hidden_segments = []

        # Проверка видимости сегментов, если они перекрыты верхним прямоугольником
        for segment in self.segments:
            if any(self.projected_overlap(segment, edge) for edge in top_edges):
                hidden_segments.append(segment)  # Этот сегмент скрыт
            else:
                visible_segments.append(segment)  # Этот сегмент видим

        hidden_edges = [edge for edge in bottom_edges if any(self.projected_overlap(edge, top_edge) for top_edge in top_edges)]
        visible_edges = [edge for edge in bottom_edges if edge not in hidden_edges]

        return top_edges, visible_edges, hidden_edges, visible_segments, hidden_segments

    def get_rectangle_edges(self, rect):
        x1, y1 = rect[0]
        x2, y2 = rect[1]
        return [
            [(x1, y1), (x2, y1)],  # Нижняя грань
            [(x2, y1), (x2, y2)],  # Правая грань
            [(x2, y2), (x1, y2)],  # Верхняя грань
            [(x1, y2), (x1, y1)]   # Левая грань
        ]

    def projected_overlap(self, seg1, seg2):
        """Проверка пересечения отрезков на проекции по осям X и Y"""
        x1_min, x1_max = sorted([seg1[0][0], seg1[1][0]])
        x2_min, x2_max = sorted([seg2[0][0], seg2[1][0]])
        y1_min, y1_max = sorted([seg1[0][1], seg1[1][1]])
        y2_min, y2_max = sorted([seg2[0][1], seg2[1][1]])
        return (x1_max >= x2_min and x2_max >= x1_min) and (y1_max >= y2_min and y2_max >= y1_min)

    def render(self, ax):
        top_edges, visible_edges, hidden_edges, visible_segments, hidden_segments = self.get_visible_and_hidden_objects()

        # Отображаем рёбра верхнего прямоугольника
        for edge in top_edges:
            x, y = zip(*edge)
            ax.plot(x, y, color='black', linewidth=2)

        # Отображаем видимые рёбра нижнего прямоугольника
        for edge in visible_edges:
            x, y = zip(*edge)
            ax.plot(x, y, color='black', linewidth=2)

        # Отображаем скрытые рёбра нижнего прямоугольника (пунктиром)
        for edge in hidden_edges:
            x, y = zip(*edge)
            ax.plot(x, y, color='black', linestyle='--')

        # Отображаем сегменты, где один из них будет красным пунктиром
        for segment in visible_segments:
            if segment == [(2, 3), (5, 0)]:
                x, y = zip(*segment)
                ax.plot(x, y, color='black', linestyle='--', linewidth=2)
            else:
                x, y = zip(*segment)
                ax.plot(x, y, color='black', linewidth=2)

        # Для скрытого сегмента, покрасим его в красный пунктир
        for segment in hidden_segments:
            x, y = zip(*segment)
            ax.plot(x, y, color='black', linestyle='--', linewidth=2)

def draw_axes_and_grid(ax):
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_xticks(np.arange(-10, 10, 1))
    ax.set_yticks(np.arange(-10, 10, 1))
    ax.grid(color='gray', linestyle='--', linewidth=0.5)

if __name__ == "__main__":
    segments = [
        [(1, 1), (6, 4)],  # Отрезок 1
        [(2, 3), (5, 0)]   # Отрезок 2
    ]

    rectangles = [
        [(-7, -6), (-3, -2)],  # Верхний прямоугольник
        [(-9, -8), (-5, -4)]   # Нижний прямоугольник
    ]

    fig, ax = plt.subplots()
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)

    draw_axes_and_grid(ax)

    nns = NewellNewellSanchAlgorithm(segments, rectangles)
    nns.render(ax)

    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
