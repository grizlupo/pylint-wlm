'''pylint plugin for wlm
suppress undefined-variable message in logic block.

install in the vscode

    "python.linting.pylintArgs": [
        "--load-plugins=pylint_wlm"
    ]
'''


from astroid.node_classes import Name
from pylint.checkers import utils
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker


class WithInlineChecker(BaseChecker):
    """wlm의 로직부분에 대한 pylint의 undefined-variable 에러를 껀다.
    로직의 변수들은 소유관계에 의해 참조되므로 파이썬 문법으로는 정의되지 않은 변수다.
    로직과 파이썬 코드는 함께하므로
    로직부분임을 감지해서 부분적으로 undefined-variable를 억제시킨다.
    """    
    __implements__ = IAstroidChecker

    name = 'wlm'
    priority = -1
    msgs = {
        'E8001': (
            'suppress undefined-variable message in logic block.',
            'suppress-logic-undefined-variable',
            'suppress undefined-variable message in logic block.')}

    def _suppress(self, node):
        for lineno in range(node.fromlineno, node.tolineno + 1):
            self.linter.disable('undefined-variable', 'module', lineno)
            self.linter.disable('bad-exception-context', 'module', lineno)

    @utils.check_messages('suppress-logic-undefined-variable')
    def visit_functiondef(self, node):
        # @logic으로 데코레이션된 함수
        decolst = node.decorators.nodes
        if len(decolst) == 1:
            deco = decolst[0]
            if isinstance(deco, Name) and deco.name == 'logic':
                self._suppress(node)

    @utils.check_messages('suppress-logic-undefined-variable')
    def visit_with(self, node):
        # with code:
        context = node.items[0][0]
        if isinstance(context, Name) and context.name == 'code':
            self._suppress(node)


def register(linter):
    linter.register_checker(WithInlineChecker(linter))
