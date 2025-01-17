import typing as tp

from PyQt5.QtWidgets import QMenu


class Menu(QMenu):

    @staticmethod
    def add_menu(
            menu: QMenu,
            name: str
    ) -> QMenu:
        sub = menu.addMenu(name)
        return sub

    @staticmethod
    def add_action(
            menu: QMenu,
            name: str,
            handler: tp.Callable,
            tip: tp.Optional[str] = None,
            checked: tp.Optional[bool] = None
    ):
        action = menu.addAction(name)
        action.triggered.connect(handler)
        if tip is not None:
            action.setToolTip(tip)
        if checked is not None:
            action.setCheckable(True)
            action.setChecked(checked)
        return action
