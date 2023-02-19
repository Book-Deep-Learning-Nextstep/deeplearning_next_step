import os
from typing import Union

import pytorch_lightning as pl
import wandb
from omegaconf import DictConfig
from torch import optim


def flatten_dict(input_dict: Union[dict, DictConfig], separator="_", prefix=""):
    """flattening dict,
    used in wandb log.
    """
    if isinstance(input_dict, DictConfig):
        input_dict = dict(input_dict)
    return (
        {
            prefix + separator + k if prefix else k: v
            for kk, vv in input_dict.items()
            for k, v in flatten_dict(vv, separator, kk).items()
        }
        if isinstance(input_dict, dict)
        else {prefix: input_dict}
    )


def configure_optimizer_element(
    opt_cfg: DictConfig, lr_sch_cfg: DictConfig, update_parameters
):
    optimizer = None
    scheduler = None
    # setup optimizer
    _optimizer = getattr(optim, opt_cfg.name, None)
    if _optimizer is None:
        raise NotImplementedError(f"Not supported optimizer: {opt_cfg.name}")
    else:
        optimizer = _optimizer(update_parameters, **opt_cfg.kwargs)

    # setup lr scheduler
    if lr_sch_cfg.name is None or lr_sch_cfg.name == "":
        pass
    elif getattr(optim.lr_scheduler, lr_sch_cfg.name, None) is not None:
        scheduler = getattr(optim.lr_scheduler, lr_sch_cfg.name, None)(
            optimizer, **lr_sch_cfg.kwargs
        )
    else:
        raise NotImplementedError(f"Not supported lr_scheduler: {lr_sch_cfg.name}")

    return optimizer, scheduler


# loggers
def get_loggers(cfg: DictConfig):
    logger = []
    loggers_cfg = cfg.log.loggers
    for name, kwargs_dict in loggers_cfg.items():
        if name == "WandbLogger":
            wandb.finish()
            os.makedirs(kwargs_dict.save_dir, exist_ok=True)
            logger.append(
                pl.loggers.WandbLogger(
                    config=flatten_dict(cfg),
                    # reinit=True,
                    settings=wandb.Settings(start_method="thread"),
                    **kwargs_dict,
                )
            )
        elif name == "TensorBoardLogger":
            logger.append(pl.loggers.TensorBoardLogger(**kwargs_dict))
        else:
            raise NotImplementedError(f"invalid loggers_cfg name {name}")

    return logger


# callbacks
def get_callbacks(cfg: DictConfig):
    callbacks = []
    callbacks_cfg = cfg.log.callbacks

    for name, kwargs_dict in callbacks_cfg.items():
        if name == "ModelCheckpoint":
            callbacks.append(
                pl.callbacks.ModelCheckpoint(
                    **kwargs_dict,
                )
            )
        elif name == "EarlyStopping":
            callbacks.append(pl.callbacks.EarlyStopping(**kwargs_dict))
        else:
            raise NotImplementedError(f"invalid callbacks_cfg name {name}")

    return callbacks
