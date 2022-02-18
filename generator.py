from bs4 import BeautifulSoup
from bs4 import Tag

class SVGEditor:
    def __init__(self, filename: str, title: str = "Title", 
                 subtitle: str = "Subtitle"):
        self.legend_y = 867
        self.title_y = 837
        self.curve_radius = 5
        with open(filename, 'r') as file:
            self.soup = BeautifulSoup(file, "xml")
        self.set_title_and_legend(title, subtitle)

    def set_title_and_legend(self, title: str, subtitle: str):
        """
        Sets a title and legend to the SVG.
        """
        title_container = self.soup.find("g", id = "title")
        title_container.string = ""

        title_tag = self.soup.new_tag("text", x = "10", 
            y = self.title_y, id = "tttitle", fill = "#001e0d")
        title_tag["font-size"] = "20"
        title_tag["font-weight"] = "bold"
        title_tag["font-family"] = "Arial"
        title_tag.append(title)
        title_container.append(title_tag)

        subtitle_tag = self.soup.new_tag("text", x = "10", 
            y = self.title_y + 20, id = "ttupd", fill = "#001e0d")
        subtitle_tag["font-size"] = "10"
        subtitle_tag["font-weight"] = "bold"
        subtitle_tag["font-family"] = "Arial"
        subtitle_tag.append(subtitle)
        title_container.append(subtitle_tag)
        self.soup.find("title").string = title

    def add_new_route(self, name: str, color: str):
        """
        Adds a new metro line to SVG
        """
        rect = self.soup.new_tag("rect", x = "10", y = self.legend_y, 
            fill = color, width = "313", height = "12.5")
        self.soup.find("g", id = "lgcolorbox").append(rect)
        
        text = self.soup.new_tag("text", x = "20", 
            y = self.legend_y + 10, id = f"label{name}")
        text["font-weight"] = "bold"
        text["font-size"] = "11"
        text.append(name)
        self.soup.find("g", id = "lglabels").append(text)
        self.legend_y += 12.5

    def add_new_graph(self, graph_id: str, is_dotted = False, **attributes) -> Tag:
        """
        Adds a new graph container to the SVG.
        """
        new_g = self.soup.new_tag("g", **attributes)
        if is_dotted: new_g["stroke-dasharray"] = "4, 4"
        self.soup.find("g", id = graph_id).append(new_g)
        return new_g

    def add_new_path(self, graph_id: str, path: str) -> Tag:
        """
        Adds a new path to a graph container.
        """
        new_path = self.soup.new_tag("path", d = path)
        self.soup.find("g", id = graph_id).append(new_path)
        return new_path

    def link_points(self, graph_id: str, points: list) -> Tag:
        """
        Links points to a graph container.
        """
        def define_curve(is_horizontal, is_down, is_right):
            result = ""
            c = self.curve_radius
            if is_horizontal:
                if is_down and is_right:
                    result = f"s{c} 0, {c} {c}"
                elif is_down and not is_right:
                    result = f"s-{c} 0, -{c} {c}"
                elif not is_down and not is_right:
                    result = f"s-{c} 0, -{c} -{c}"
                else:
                    result = f"s{c} 0, {c} -{c}"
            else:
                if is_down and is_right: 
                    result = f"s0 {c}, {c} {c}"
                elif is_down and not is_right:
                    result = f"s0 {c}, -{c} {c}"
                elif not is_down and not is_right: 
                    result = f"s0 -{c}, -{c} -{c}"
                else:
                    result = f"s0 -{c}, {c} -{c}"
            return result

        if len(points) <= 1: return

        c = self.curve_radius
        last_x, last_y = points[0]
        path = [f"m{last_x} {last_y}"]
        for x, y in points[1:]:
            x_diff = x - last_x
            y_diff = y - last_y
            last_x, last_y = x, y
            is_horizontal = abs(x_diff) > abs(y_diff)
            curve = define_curve(is_horizontal, y_diff > 0, x_diff > 0)
            if is_horizontal:
                if y_diff == 0:
                    path.append(f"h{x_diff}")
                else:
                    x_diff = x_diff - c if x_diff > 0 else x_diff + c
                    y_diff = y_diff - c if y_diff > 0 else y_diff + c
                    path.append(f"h{x_diff} {curve}  v{y_diff}")
            else:
                if x_diff == 0:
                    path.append(f"v{y_diff}")
                else:
                    x_diff = x_diff - c if x_diff > 0 else x_diff + c
                    y_diff = y_diff - c if y_diff > 0 else y_diff + c
                    path.append(f"v{y_diff} {curve} h{x_diff}")

        self.add_new_path(graph_id, " ".join(path))


    def save(self, filename: str):
        """
        Saves the SVG to a file.
        """
        with open(filename, 'w') as file:
            file.write(self.soup.prettify())

if __name__ == "__main__":
    editor = SVGEditor("assets/image.svg", "Paris Metro Map", 
                       "Intelligent Systems project")
    editor.add_new_route("East West Line (EW)", "#009645")
    editor.add_new_route("North South Line (NS)", "#d42e12")

    new_graph = editor.add_new_graph("lines", id = "ew", stroke = "#009645")
    editor.link_points("ew", [
        (1334, 694), (1283, 524.5),
        (1245, 634), (1186, 659),
        (1126, 659), (1066, 659),
        (974, 660), (950.5, 675),
        (926, 699), (698.5, 856),
        (630, 748), (595.5, 714),
        (554.7, 673), (519, 637),
        (451, 570), (405, 524),
        (247, 514), (202, 514),
        (155, 514), (75, 540),
        (75, 568), (75, 596),
        (75, 624), (75, 652),
        (75, 680),
    ])

    new_graph = editor.add_new_graph("lines", id = "stns_ns", stroke = "#d42e12")
    editor.link_points("stns_ns", [
        (286, 413), (286, 321),
        (286, 123), (286, 226),
        (352, 67), (435, 67),
        (632, 67), (735, 67),
        (786, 104), (786, 153),
        (786, 202), (786, 250),
        (786, 306), (786, 428),
        (770, 467), (739, 498),
        (660, 586), (702, 632),
        (833, 955),
    ])

    new_graph = editor.add_new_graph("lines", id = "stns_ne", stroke = "#9900aa")
    editor.link_points("stns_ne", [
        (723.5, 724.5), (807.5, 578.4),
        (834, 552), (861, 525),
        (888, 498), (956, 430),
        (983, 403.5), (1018, 368),
    ])

    new_graph = editor.add_new_graph("lines", id = "stns_cc", stroke = "#fa9e0d")
    editor.link_points("stns_cc", [
        (824, 739), (880, 795),
        (970, 786), (985, 754.5),
        (996, 720.5), (1003, 687),
        (984.5, 552), (964, 514),
        (854, 416), (721, 390.8), 
        (515.5, 514), (497, 549), 
        (475.7, 637), (476, 674), 
        (481, 709), (493.5, 750), 
        (513.8, 792), (540, 827.5),
    ])

    new_graph = editor.add_new_graph("lines", id = "stns_dt", stroke = "#005ec4")
    editor.link_points("stns_dt", [
        (479, 268), (479, 309),
        (479, 353), (485, 406),
        (502, 425), (524, 447.5),
        (658, 486), (818, 645),
        (804, 866), (742, 803),
        (703.5, 727), (832, 693),
        (865, 659.8), (896, 629),
        (927, 602.5), (969, 600),
        (1046, 600), (1089, 600),
        (1129, 600), (1172.5, 600),
        (1211, 600), (1286, 632),
        (1286, 667),
    ])

    new_graph = editor.add_new_graph("lines", id = "stns_te", stroke = "#784008")
    editor.link_points("stns_te", [
        (496, 34), (579, 117),
        (624, 161.8), (658, 208),
        (658, 247), (658, 309.5),
        (658, 357),
    ])

    new_graph = editor.add_new_graph("lines", True, id = "stns_ints", stroke = "#000000")
    editor.link_points("stns_ints", [
        (760.2, 689), (793, 913.3),
        (887, 871), (941.3, 821),
        (658, 402.8), (1004, 659),
        (1000, 600), (923, 463.2),
        (786, 394), (548, 471.5),
        (481, 599), (581, 866),
        (1286, 694), (1245, 600.5),
        (1227, 659), (899, 726),
        (830.3, 790), (799, 822),
        (657, 790.5), (286, 514),
        (693.5, 754), (780, 606.5),
        (1080.7, 305.3), (1177, 209.5),
        (286, 225.5), (705, 532),
        (720, 547), (479, 225.5),
        (479, 242), (529, 67),
    ])

    editor.save("result.svg")
