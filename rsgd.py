from torch.optim.optimizer import Optimizer, required


class RiemannianSGD(Optimizer):
    # gradient w przestrzeni hiperbolicznej - Riemannowski SGD

    def __init__(
            self,
            params,
            lr=required,
            rgrad=required,
            expm=required,
    ):
        defaults = {
            'lr': lr,
            'rgrad': rgrad,
            'expm': expm,
        }
        super(RiemannianSGD, self).__init__(params, defaults)

    def step(self, lr=None, counts=None, **kwargs):
        loss = None

        for group in self.param_groups:
            for p in group['params']:
                lr = lr or group['lr']
                rgrad = group['rgrad']
                expm = group['expm']

                if p.grad is None:
                    continue
                d_p = p.grad.data
                # make sure we have no duplicates in sparse tensor
                if d_p.is_sparse:
                    d_p = d_p.coalesce()
                d_p = rgrad(p.data, d_p)
                d_p.mul_(-lr)
                expm(p.data, d_p)

        return loss