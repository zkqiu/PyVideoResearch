"""
Asynchronous Temporal Fields Base model
"""
import torch.nn as nn
import torch
from wrapper import Wrapper


class AsyncTFBase(Wrapper):
    def __init__(self, basenet, args):
        super(AsyncTFBase, self).__init__(basenet, args)
        nclasses, nhidden = args.nclass, args.nhidden
        self.mA = basenet
        self.nc = nclasses
        # self.mAA = nn.Linear(1, nclasses * nclasses)
        self.naa = nhidden
        # self.mAAa = nn.Sequential(nn.Linear(1, self.nc * self.naa, bias=False),
        #                           nn.Dropout())
        # self.mAAb = nn.Sequential(nn.Linear(1, self.naa * self.nc, bias=False),
        #                           nn.Dropout())
        self.mAAa = nn.Linear(1, self.nc * self.naa, bias=False)
        self.mAAb = nn.Linear(1, self.naa * self.nc, bias=False)

    def forward(self, x, meta):
        a = self.mA(x)
        const = torch.ones(a.shape[0], 1).cuda()
        # aa = self.mAA(const)
        aaa = self.mAAa(const).view(-1, self.nc, self.naa)
        aab = self.mAAb(const).view(-1, self.naa, self.nc)
        aa = torch.bmm(aaa, aab)

        # aa = torch.zeros(*aa.shape)
        # for i in range(a.shape[0]):
        #     aa[i, :] = torch.eye(a.shape[1])[:]
        # aa = Variable(aa.cuda())

        return a, aa.view(-1, self.nc, self.nc)
