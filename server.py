import cherrypy as cp
from classes import BancoDeFilmes


def realizar_conexoes(desp):
    banco = BancoDeFilmes()
    desp.connect(name='MovieReg', route='/filme', controller=banco, action='criar_filme', conditions=dict(method=['POST']))
    desp.connect(name='MovieList', route='/filme', controller=banco, action='listar_filmes', conditions=dict(method=['GET']))
    desp.connect(name='MovieEdit', route='/filme/:id', controller=banco, action='editar_filme', conditions=dict(method=['PATCH']))
    desp.connect(name='MovieRemove', route='/filme/:id', controller=banco, action='remover_filme', conditions=dict(method=['DELETE']))


def main():
    desp = cp.dispatch.RoutesDispatcher()

    realizar_conexoes(desp)

    conf = {'/': {'request.dispatch': desp}}
    cp.tree.mount(root=None, config=conf, )
    cp.config.update({'server.socket_port': 9092})
    cp.engine.start()
    cp.engine.block()


if __name__ == "__main__":
    main()