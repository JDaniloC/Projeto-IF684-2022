from bs4 import BeautifulSoup
from bs4 import Tag

class SVGEditor:
    def __init__(self, filename: str, title: str = "Title", 
                 subtitle: str = "Subtitle"):
        self.title_x = 600
        self.title_y = 30
        self.legend_y = 50
        self.curve_radius = 5
        self.points_added = set()
        with open(filename, 'r') as file:
            self.soup = BeautifulSoup(file, "xml")
        self.set_title_and_legend(title, subtitle)

    def set_title_and_legend(self, title: str, subtitle: str):
        """
        Sets a title and legend to the SVG.
        """
        title_container = self.soup.find("g", id = "title")
        title_container.string = ""

        title_tag = self.soup.new_tag("text", x = self.title_x, 
            y = self.title_y, id = "tttitle", fill = "#001e0d")
        title_tag["font-size"] = "20"
        title_tag["font-weight"] = "bold"
        title_tag["font-family"] = "Arial"
        title_tag.append(title)
        title_container.append(title_tag)

        subtitle_tag = self.soup.new_tag("text", x = self.title_x, 
            y = self.title_y + 10, id = "ttupd", fill = "#001e0d")
        subtitle_tag["font-size"] = "10"
        subtitle_tag["font-weight"] = "bold"
        subtitle_tag["font-family"] = "Arial"
        subtitle_tag.append(subtitle)
        title_container.append(subtitle_tag)
        self.soup.find("title").string = title

        rect = self.soup.new_tag("rect", x = self.title_x - 10, 
            y = self.title_y - 20, height = "295", width = "333", 
            fill = "#f2f2f2", id = "lgbox")
        self.soup.find("g", id = "legend").insert(0, rect)

    def add_new_route(self, name: str, color: str, stations: list) -> str:
        """
        Adds a new metro line to SVG
        """
        route_id = name.replace(" ", "_")
        rect = self.soup.new_tag("rect", x = self.title_x, y = self.legend_y, 
            fill = color, width = "313", height = "12.5")
        self.soup.find("g", id = "lgcolorbox").append(rect)
        
        text = self.soup.new_tag("text", x = self.title_x + 10, 
            y = self.legend_y + 10, id = f"label{route_id}")
        text["font-weight"] = "bold"
        text["font-size"] = "11"
        text.append(name)
        self.soup.find("g", id = "lglabels").append(text)
        self.legend_y += 12.5

        anchor = self.soup.new_tag("a", fill = "#ffffff")
        anchor["xlink:href"] = f"#{route_id}"

        positions = self.soup.new_tag("g", id = f"stns_{route_id}", stroke = color)
        labels = self.soup.new_tag("g", id = f"lb{route_id}", fill = "#000000")

        for station in stations:
            station_name, x, y = station
            if station_name in self.points_added:
                continue
            self.points_added.add(station_name)
            
            formatted_id = station_name.replace(" ", "_")
            circle = self.soup.new_tag("circle", r = 3, cx = x, 
                                       cy = y, id = formatted_id)
            
            text = self.soup.new_tag("text", x = x - 15, y = y + 15, 
                                     id = f"lb{formatted_id}")
            text["font-size"] = "12"
            text.append(station_name)
            labels.append(text)

            positions.append(circle)

        anchor.append(positions)
        self.soup.find("g", id = "stns_labels").append(labels)
        self.soup.find("g", id = "stns_icons").append(anchor)
        return route_id

    def add_new_path(self, graph_id: str, path: str) -> Tag:
        """
        Adds a new path to a graph container.
        """
        new_path = self.soup.new_tag("path", d = path)
        self.soup.find("g", id = graph_id).append(new_path)
        return new_path

    def link_points(self, graph_id: str, color: str, points: list, 
        edge_costs: dict = {}, is_dotted:bool = False) -> Tag:
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

        def write_cost(middle_x: int, middle_y: int):
            if last_name in edge_costs:
                cost = list(filter(lambda x: x[0] == name, edge_costs[last_name]))
                if len(cost) > 0:
                    cost = cost[0][1]
                    text = self.soup.new_tag("text", x = middle_x, 
                                             y = middle_y, fill = color)
                    text["font-size"] = "12"
                    text.append(f"({cost})")
                    labels.append(text)

        new_graph = self.soup.new_tag("g", id = graph_id, stroke = color)
        if is_dotted: new_graph["stroke-dasharray"] = "4, 4"

        if len(points) <= 1: return
        labels = self.soup.new_tag("g", id = f"ed{graph_id}", fill = "#000000")

        c = self.curve_radius
        last_name, last_x, last_y = points[0]
        path = [f"m{last_x} {last_y}"]
        for name, x, y in points[1:]:
            x_diff = x - last_x
            y_diff = y - last_y
            
            is_horizontal = abs(x_diff) > abs(y_diff)
            curve = define_curve(is_horizontal, y_diff > 0, x_diff > 0)
            
            if is_horizontal:
                if y_diff == 0:
                    path.append(f"h{x_diff}")
                    write_cost((x + last_x) / 2 + 5, (y + last_y) / 2 + 5)
                else:
                    x_diff = x_diff - c if x_diff > 0 else x_diff + c
                    y_diff = y_diff - c if y_diff > 0 else y_diff + c
                    path.append(f"h{x_diff} {curve}  v{y_diff}")

                    write_cost((x + last_x + x_diff) / 2 + 10, 
                               (y + last_y + y_diff) / 2 - 5)
            else:
                if x_diff == 0:
                    path.append(f"v{y_diff}")
                    write_cost((x + last_x) / 2 + 5, (y + last_y) / 2 + 5)
                else:
                    x_diff = x_diff - c if x_diff > 0 else x_diff + c
                    y_diff = y_diff - c if y_diff > 0 else y_diff + c
                    path.append(f"v{y_diff} {curve} h{x_diff}")

                    write_cost((x + last_x + x_diff) / 2 - 30, 
                               (y + last_y + y_diff) / 2 - 10)
            
            last_name, last_x, last_y = name, x, y

        new_path = self.soup.new_tag("path", d = " ".join(path))
        new_graph.append(new_path)
        self.soup.find("g", id = "lines").append(new_graph)
        self.soup.find("g", id = "edges_labels").append(labels)

    def save(self, filename: str):
        """
        Saves the SVG to a file.
        """
        with open(filename, 'w') as file:
            file.write(self.soup.prettify())

if __name__ == "__main__":
    editor = SVGEditor("assets/image.svg", "Paris Metro Map", 
                       "Intelligent Systems project")
    stations = [
        ("Expo", 1334, 694), 
        ("Changi", 1283, 524.5),
        ("Airport", 1245, 634), 
        ("Pasir Ris", 1186, 659),
        ("Tampines", 1126, 659), 
        ("Simei", 1066, 659),
        ("Bedok", 974, 660), 
        ("Kembangan", 950.5, 675),
        ("Eunos", 926, 699), 
        ("Aljunied", 698.5, 856),
        ("Kallang", 630, 748), 
        ("Lavender", 595.5, 714),
        ("Tanjong", 554.7, 673), 
    ]
    route_id = editor.add_new_route("East West Line (EW)", "#009645", stations)
    editor.link_points(route_id, "#009645", stations)

    editor.save("result.svg")
