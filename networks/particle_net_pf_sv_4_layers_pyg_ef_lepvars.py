import torch
from utils.nn.model.ParticleNetPyG_lepvars import ParticleNetTaggerPyG
from utils.nn.model.ParticleNetPyGJittable import ParticleNetTaggerPyGJittable


def get_model(data_config, jittable=False, **kwargs):
    conv_params = [
        (16, (64, 64, 64)),
        (16, (128, 128, 128)),
        (16, (256, 256, 256)),
        (16, (256, 256, 256)),
    ]
    fc_params = [(256, 0.1)]
    use_fusion = True

    pf_features_dims = len(data_config.input_dicts["pf_features"])
    sv_features_dims = len(data_config.input_dicts["sv_features"])
    el_features_dims = len(data_config.input_dicts["el_features"])
    mu_features_dims = len(data_config.input_dicts["mu_features"])
    num_classes = len(data_config.label_value)

    pnet_model = ParticleNetTaggerPyGJittable if jittable else ParticleNetTaggerPyG

    model = pnet_model(
        pf_features_dims,
        sv_features_dims,
        el_features_dims,
        mu_features_dims,
        num_classes,
        conv_params,
        fc_params,
        use_fusion=use_fusion,
        use_fts_bn=kwargs.get("use_fts_bn", False),
        use_counts=kwargs.get("use_counts", True),
        pf_input_dropout=kwargs.get("pf_input_dropout", 0.0),
        sv_input_dropout=kwargs.get("sv_input_dropout", 0.0),
        el_input_dropout=kwargs.get("el_input_dropout", 0.0),
        mu_input_dropout=kwargs.get("mu_input_dropout", 0.0),
        for_inference=kwargs.get("for_inference", False),
        use_edge_feats=True,
    )

    model_info = {
        "input_names": list(data_config.input_names),
        "input_shapes": {k: ((1,) + s[1:]) for k, s in data_config.input_shapes.items()},
        "output_names": ["softmax"],
        "dynamic_axes": {
            **{k: {0: "N", 2: "n_" + k.split("_")[0]} for k in data_config.input_names},
            **{"softmax": {0: "N"}},
        },
    }

    return model, model_info


def get_loss(data_config, **kwargs):
    return torch.nn.CrossEntropyLoss()
