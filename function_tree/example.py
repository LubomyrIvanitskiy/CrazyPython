from function_tree import accessed_by


def build_model():
    build_autoencoder()
    build_classifier()
    ...


with accessed_by(build_model):
    def build_autoencoder():
        encoder = build_encoder()
        decoder = build_decoder()


    with accessed_by(build_autoencoder):
        def build_encoder():
            pass


        def build_decoder():
            pass


    def build_classifier():
        encoder = build_encoder()
        mlp = build_mlp()
        ...


    with accessed_by(build_classifier):
        def build_mlp():
            pass
