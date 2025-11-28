"""
Automata Visualizer Pro - PyQt5 GUI (View/Controller)
"""

import sys
import json
import math
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QSplitter, QTabWidget, QWidget, QVBoxLayout,
    QHBoxLayout, QTextEdit, QPushButton, QLineEdit, QLabel, QGraphicsView,
    QGraphicsScene, QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsLineItem,
    QGraphicsPolygonItem, QMessageBox, QListWidget, QListWidgetItem,
    QGraphicsPathItem
)
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QBrush, QColor, QPolygonF, QPainter, QFont, QPainterPath

from dfa_logic import DFA, SAMPLE_DFA_DATA

DARK_STYLE = """
QMainWindow, QWidget { background-color: #2b2b2b; color: #e0e0e0; }
QTextEdit, QLineEdit, QListWidget { background-color: #3c3c3c; color: #e0e0e0; border: 1px solid #555; border-radius: 4px; padding: 4px; }
QPushButton { background-color: #4a4a4a; color: #e0e0e0; border: 1px solid #666; border-radius: 4px; padding: 8px 16px; }
QPushButton:hover { background-color: #5a5a5a; }
QPushButton:pressed { background-color: #3a3a3a; }
QTabWidget::pane { border: 1px solid #555; background-color: #2b2b2b; }
QTabBar::tab { background-color: #3c3c3c; color: #e0e0e0; padding: 8px 16px; border: 1px solid #555; }
QTabBar::tab:selected { background-color: #4a4a4a; }
QLabel { color: #e0e0e0; }
QGraphicsView { background-color: #1e1e1e; border: 1px solid #555; }
QSplitter::handle { background-color: #555; }
"""


class StateNode(QGraphicsEllipseItem):
    def __init__(self, name, x, y, radius=30, is_final=False):
        super().__init__(-radius, -radius, radius * 2, radius * 2)
        self.name = name
        self.radius = radius
        self.is_final = is_final
        self.setPos(x, y)
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable, True)
        self.setFlag(QGraphicsEllipseItem.ItemSendsGeometryChanges, True)
        self.setPen(QPen(QColor("#00bcd4"), 2))
        self.setBrush(QBrush(QColor("#3c3c3c")))
        self.label = QGraphicsTextItem(name, self)
        self.label.setDefaultTextColor(QColor("#e0e0e0"))
        self.label.setFont(QFont("Arial", 10, QFont.Bold))
        rect = self.label.boundingRect()
        self.label.setPos(-rect.width() / 2, -rect.height() / 2)
        self.inner_circle = None
        if is_final:
            inner_radius = radius - 6
            self.inner_circle = QGraphicsEllipseItem(
                -inner_radius, -inner_radius, inner_radius * 2, inner_radius * 2, self
            )
            self.inner_circle.setPen(QPen(QColor("#00bcd4"), 2))
            self.inner_circle.setBrush(QBrush(Qt.NoBrush))
        self.transitions = []

    def set_highlight(self, highlighted):
        if highlighted:
            self.setBrush(QBrush(QColor("#00bcd4")))
            self.label.setDefaultTextColor(QColor("#1e1e1e"))
        else:
            self.setBrush(QBrush(QColor("#3c3c3c")))
            self.label.setDefaultTextColor(QColor("#e0e0e0"))

    def itemChange(self, change, value):
        if change == QGraphicsEllipseItem.ItemPositionHasChanged:
            for trans in self.transitions:
                trans.update_position()
        return super().itemChange(change, value)


class TransitionArrow:
    def __init__(self, scene, from_node, to_node, symbol):
        self.scene = scene
        self.from_node = from_node
        self.to_node = to_node
        self.symbol = symbol
        self.line = None
        self.arrow_head = None
        self.label = None
        self.is_self_loop = from_node == to_node
        from_node.transitions.append(self)
        if to_node != from_node:
            to_node.transitions.append(self)
        self.draw()

    def draw(self):
        if self.line:
            self.scene.removeItem(self.line)
        if self.arrow_head:
            self.scene.removeItem(self.arrow_head)
        if self.label:
            self.scene.removeItem(self.label)

        pen = QPen(QColor("#ff9800"), 2)

        if self.is_self_loop:
            cx, cy = self.from_node.pos().x(), self.from_node.pos().y()
            r = self.from_node.radius
            path = QPainterPath()
            loop_size = 25
            path.moveTo(cx - 10, cy - r)
            path.cubicTo(cx - 30, cy - r - loop_size * 2, cx + 30, cy - r - loop_size * 2, cx + 10, cy - r)
            self.line = QGraphicsPathItem(path)
            self.line.setPen(pen)
            self.scene.addItem(self.line)
            arrow_x, arrow_y = cx + 10, cy - r
            self.arrow_head = self._create_arrow_head(cx + 5, cy - r - 15, arrow_x, arrow_y)
            self.scene.addItem(self.arrow_head)
            self.label = QGraphicsTextItem(self.symbol)
            self.label.setDefaultTextColor(QColor("#ff9800"))
            self.label.setFont(QFont("Arial", 9, QFont.Bold))
            self.label.setPos(cx - 8, cy - r - loop_size * 2 - 10)
            self.scene.addItem(self.label)
        else:
            x1, y1 = self.from_node.pos().x(), self.from_node.pos().y()
            x2, y2 = self.to_node.pos().x(), self.to_node.pos().y()
            angle = math.atan2(y2 - y1, x2 - x1)
            r1, r2 = self.from_node.radius, self.to_node.radius
            start_x = x1 + r1 * math.cos(angle)
            start_y = y1 + r1 * math.sin(angle)
            end_x = x2 - r2 * math.cos(angle)
            end_y = y2 - r2 * math.sin(angle)
            self.line = QGraphicsLineItem(start_x, start_y, end_x, end_y)
            self.line.setPen(pen)
            self.scene.addItem(self.line)
            self.arrow_head = self._create_arrow_head(start_x, start_y, end_x, end_y)
            self.scene.addItem(self.arrow_head)
            mid_x, mid_y = (start_x + end_x) / 2, (start_y + end_y) / 2
            offset = 15
            perp_angle = angle + math.pi / 2
            label_x = mid_x + offset * math.cos(perp_angle) - 5
            label_y = mid_y + offset * math.sin(perp_angle) - 10
            self.label = QGraphicsTextItem(self.symbol)
            self.label.setDefaultTextColor(QColor("#ff9800"))
            self.label.setFont(QFont("Arial", 9, QFont.Bold))
            self.label.setPos(label_x, label_y)
            self.scene.addItem(self.label)

    def _create_arrow_head(self, x1, y1, x2, y2):
        angle = math.atan2(y2 - y1, x2 - x1)
        arrow_size = 10
        p1 = QPointF(x2, y2)
        p2 = QPointF(x2 - arrow_size * math.cos(angle - math.pi / 6), y2 - arrow_size * math.sin(angle - math.pi / 6))
        p3 = QPointF(x2 - arrow_size * math.cos(angle + math.pi / 6), y2 - arrow_size * math.sin(angle + math.pi / 6))
        polygon = QPolygonF([p1, p2, p3])
        arrow = QGraphicsPolygonItem(polygon)
        arrow.setPen(QPen(QColor("#ff9800")))
        arrow.setBrush(QBrush(QColor("#ff9800")))
        return arrow

    def update_position(self):
        self.draw()


class StartArrow:
    def __init__(self, scene, node):
        self.scene = scene
        self.node = node
        self.line = None
        self.arrow_head = None
        node.transitions.append(self)
        self.draw()

    def draw(self):
        if self.line:
            self.scene.removeItem(self.line)
        if self.arrow_head:
            self.scene.removeItem(self.arrow_head)
        x, y = self.node.pos().x(), self.node.pos().y()
        r = self.node.radius
        start_x, start_y = x - r - 40, y
        end_x, end_y = x - r, y
        pen = QPen(QColor("#4caf50"), 3)
        self.line = QGraphicsLineItem(start_x, start_y, end_x, end_y)
        self.line.setPen(pen)
        self.scene.addItem(self.line)
        arrow_size = 12
        p1 = QPointF(end_x, end_y)
        p2 = QPointF(end_x - arrow_size, end_y - arrow_size / 2)
        p3 = QPointF(end_x - arrow_size, end_y + arrow_size / 2)
        polygon = QPolygonF([p1, p2, p3])
        self.arrow_head = QGraphicsPolygonItem(polygon)
        self.arrow_head.setPen(QPen(QColor("#4caf50")))
        self.arrow_head.setBrush(QBrush(QColor("#4caf50")))
        self.scene.addItem(self.arrow_head)

    def update_position(self):
        self.draw()


class AutomataCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.TextAntialiasing)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.nodes = {}
        self.transitions = []
        self.start_arrow = None

    def clear_all(self):
        self.scene.clear()
        self.nodes = {}
        self.transitions = []
        self.start_arrow = None

    def draw_dfa(self, dfa):
        self.clear_all()
        states = list(dfa.states)
        n = len(states)
        if n == 0:
            return
        center_x, center_y = 300, 250
        radius = 120 if n > 1 else 0

        for i, state in enumerate(states):
            angle = 2 * math.pi * i / n - math.pi / 2
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            is_final = state in dfa.final_states
            node = StateNode(state, x, y, is_final=is_final)
            self.scene.addItem(node)
            self.nodes[state] = node

        if dfa.start_state in self.nodes:
            self.start_arrow = StartArrow(self.scene, self.nodes[dfa.start_state])

        # Group transitions by (from, to) to combine labels
        transition_symbols = {}
        for from_state, trans in dfa.transitions.items():
            for symbol, to_state in trans.items():
                key = (from_state, to_state)
                if key in transition_symbols:
                    transition_symbols[key].append(symbol)
                else:
                    transition_symbols[key] = [symbol]

        for (from_state, to_state), symbols in transition_symbols.items():
            if from_state in self.nodes and to_state in self.nodes:
                label = ",".join(symbols)
                arrow = TransitionArrow(self.scene, self.nodes[from_state], self.nodes[to_state], label)
                self.transitions.append(arrow)

    def highlight_state(self, state_name, highlight=True):
        if state_name in self.nodes:
            self.nodes[state_name].set_highlight(highlight)

    def wheelEvent(self, event):
        factor = 1.15 if event.angleDelta().y() > 0 else 1 / 1.15
        self.scale(factor, factor)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Automata Visualizer Pro")
        self.setGeometry(100, 100, 1200, 700)
        self.dfa = None
        self.current_state = None
        self.test_string = ""
        self.test_index = 0
        self.setup_ui()

    def setup_ui(self):
        splitter = QSplitter(Qt.Horizontal)
        self.setCentralWidget(splitter)

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(10, 10, 10, 10)

        self.tabs = QTabWidget()
        left_layout.addWidget(self.tabs)

        # Tab 1: Definition
        def_tab = QWidget()
        def_layout = QVBoxLayout(def_tab)
        def_layout.addWidget(QLabel("DFA Definition (JSON):"))
        self.json_editor = QTextEdit()
        self.json_editor.setPlainText(json.dumps(SAMPLE_DFA_DATA, indent=2))
        self.json_editor.setFont(QFont("Consolas", 10))
        def_layout.addWidget(self.json_editor)

        btn_layout = QHBoxLayout()
        self.load_btn = QPushButton("Load DFA")
        self.load_btn.clicked.connect(self.load_dfa)
        btn_layout.addWidget(self.load_btn)
        self.minimize_btn = QPushButton("Minimize")
        self.minimize_btn.clicked.connect(self.minimize_dfa)
        btn_layout.addWidget(self.minimize_btn)
        def_layout.addLayout(btn_layout)
        self.tabs.addTab(def_tab, "Definition")

        # Tab 2: Debugger
        debug_tab = QWidget()
        debug_layout = QVBoxLayout(debug_tab)
        debug_layout.addWidget(QLabel("Test String:"))
        self.test_input = QLineEdit()
        self.test_input.setPlaceholderText("Enter string to test...")
        debug_layout.addWidget(self.test_input)

        dbg_btn_layout = QHBoxLayout()
        self.step_btn = QPushButton("Step Forward")
        self.step_btn.clicked.connect(self.step_forward)
        dbg_btn_layout.addWidget(self.step_btn)
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self.reset_debugger)
        dbg_btn_layout.addWidget(self.reset_btn)
        self.run_all_btn = QPushButton("Run All")
        self.run_all_btn.clicked.connect(self.run_all)
        dbg_btn_layout.addWidget(self.run_all_btn)
        debug_layout.addLayout(dbg_btn_layout)

        self.state_label = QLabel("Current State: -")
        self.state_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px;")
        debug_layout.addWidget(self.state_label)
        self.result_label = QLabel("Result: -")
        self.result_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px;")
        debug_layout.addWidget(self.result_label)
        self.status_label = QLabel("Status: Ready")
        self.status_label.setStyleSheet("font-size: 12px; padding: 10px; color: #888;")
        debug_layout.addWidget(self.status_label)
        debug_layout.addStretch()
        self.tabs.addTab(debug_tab, "Debugger")

        # Tab 3: Bulk Test
        bulk_tab = QWidget()
        bulk_layout = QVBoxLayout(bulk_tab)
        bulk_layout.addWidget(QLabel("Test Strings (one per line):"))
        self.bulk_input = QTextEdit()
        self.bulk_input.setPlaceholderText("Enter test strings...\n001\n101\n111")
        bulk_layout.addWidget(self.bulk_input)
        self.run_suite_btn = QPushButton("Run Suite")
        self.run_suite_btn.clicked.connect(self.run_suite)
        bulk_layout.addWidget(self.run_suite_btn)
        self.results_list = QListWidget()
        bulk_layout.addWidget(self.results_list)
        self.tabs.addTab(bulk_tab, "Bulk Test")

        splitter.addWidget(left_panel)

        # Right Panel: Canvas
        self.canvas = AutomataCanvas()
        splitter.addWidget(self.canvas)
        splitter.setSizes([400, 800])

    def load_dfa(self):
        try:
            text = self.json_editor.toPlainText()
            data = json.loads(text)
            self.dfa = DFA.from_dict(data)
            self.canvas.draw_dfa(self.dfa)
            self.reset_debugger()
            QMessageBox.information(self, "Success", "DFA loaded successfully!")
        except json.JSONDecodeError as e:
            QMessageBox.critical(self, "JSON Error", f"Invalid JSON format:\n{str(e)}")
        except ValueError as e:
            QMessageBox.critical(self, "Validation Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load DFA:\n{str(e)}")

    def reset_debugger(self):
        if self.current_state:
            self.canvas.highlight_state(self.current_state, False)
        self.test_string = self.test_input.text()
        self.test_index = 0
        if self.dfa:
            self.current_state = self.dfa.start_state
            self.canvas.highlight_state(self.current_state, True)
            self.state_label.setText(f"Current State: {self.current_state}")
        else:
            self.current_state = None
            self.state_label.setText("Current State: -")
        self.result_label.setText("Result: -")
        self.status_label.setText("Status: Ready - Press Step Forward to begin")


    def step_forward(self):
        if not self.dfa:
            QMessageBox.warning(self, "Warning", "Please load a DFA first!")
            return
        if not self.test_string:
            self.test_string = self.test_input.text()
            self.test_index = 0
            self.current_state = self.dfa.start_state
            self.canvas.highlight_state(self.current_state, True)

        if self.test_index >= len(self.test_string):
            is_accepted = self.current_state in self.dfa.final_states
            result = "ACCEPTED ✓" if is_accepted else "REJECTED ✗"
            color = "#4caf50" if is_accepted else "#f44336"
            self.result_label.setText(f"Result: {result}")
            self.result_label.setStyleSheet(f"font-size: 14px; font-weight: bold; padding: 10px; color: {color};")
            self.status_label.setText("Status: Processing complete")
            return

        char = self.test_string[self.test_index]
        prev_state = self.current_state
        next_state = self.dfa.get_transition(prev_state, char)

        if next_state:
            self.canvas.highlight_state(prev_state, False)
            self.current_state = next_state
            self.canvas.highlight_state(self.current_state, True)
            self.state_label.setText(f"Current State: {self.current_state}")
            self.status_label.setText(f"Status: Processing '{char}' -> Transitioning to {next_state}")
            self.test_index += 1
        else:
            self.status_label.setText(f"Status: No transition for '{char}' from {prev_state} - STUCK")
            self.result_label.setText("Result: REJECTED ✗ (No valid transition)")
            self.result_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px; color: #f44336;")

    def run_all(self):
        if not self.dfa:
            QMessageBox.warning(self, "Warning", "Please load a DFA first!")
            return
        self.reset_debugger()
        test_str = self.test_input.text()
        accepted, final_state, _ = self.dfa.test_string(test_str)

        if self.current_state:
            self.canvas.highlight_state(self.current_state, False)
        self.current_state = final_state
        self.canvas.highlight_state(self.current_state, True)
        self.state_label.setText(f"Current State: {self.current_state}")

        result = "ACCEPTED ✓" if accepted else "REJECTED ✗"
        color = "#4caf50" if accepted else "#f44336"
        self.result_label.setText(f"Result: {result}")
        self.result_label.setStyleSheet(f"font-size: 14px; font-weight: bold; padding: 10px; color: {color};")
        self.status_label.setText("Status: Processing complete")

    def run_suite(self):
        if not self.dfa:
            QMessageBox.warning(self, "Warning", "Please load a DFA first!")
            return
        self.results_list.clear()
        lines = self.bulk_input.toPlainText().strip().split('\n')
        for line in lines:
            test_str = line.strip()
            if not test_str:
                continue
            accepted, _, _ = self.dfa.test_string(test_str)
            status = "✓ Accepted" if accepted else "✗ Rejected"
            color = "#4caf50" if accepted else "#f44336"
            item = QListWidgetItem(f"'{test_str}' → {status}")
            item.setForeground(QColor(color))
            self.results_list.addItem(item)

    def minimize_dfa(self):
        if not self.dfa:
            QMessageBox.warning(self, "Warning", "Please load a DFA first!")
            return
        try:
            old_count = len(self.dfa.states)
            self.dfa = self.dfa.minimize()
            new_count = len(self.dfa.states)
            self.json_editor.setPlainText(json.dumps(self.dfa.to_dict(), indent=2))
            self.canvas.draw_dfa(self.dfa)
            self.reset_debugger()

            removed = old_count - new_count
            if removed > 0:
                QMessageBox.information(self, "Minimization Complete", f"Removed {removed} state(s).\nDFA has been minimized.")
            else:
                QMessageBox.information(self, "Minimization Complete", "DFA is already minimal.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Minimization failed:\n{str(e)}")


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_STYLE)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
