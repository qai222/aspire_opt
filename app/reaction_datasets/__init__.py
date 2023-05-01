import os.path

import numpy as np
import pandas as pd
from loguru import logger
from ord_schema.message_helpers import load_message, messages_to_dataframe
from ord_schema.proto.dataset_pb2 import Dataset
from pandas._typing import FilePath

"""
read datasets from ./download
"""
this_dir = os.path.dirname(os.path.abspath(__file__))
download_dir = os.path.join(this_dir, 'download')


class BenchmarkDataframe:
    def __init__(self, name: str, source: FilePath, continuous_params: list[str], categorical_params: list[str],
                 targets: list[str], df: pd.DataFrame):
        self.name = name
        self.df = df
        self.targets = targets
        self.continuous_params = continuous_params
        self.categorical_params = categorical_params
        self.source = source

    @classmethod
    def ds_0(cls, filename: FilePath = 'ds-0.xlsx'):
        source = f"{download_dir}/{filename}"
        df = pd.read_excel(source)
        df.drop(columns=['Reaction_No'], inplace=True)
        """
        ['Reactant_1_Name', 'Reactant_1_Short_Hand', 'Reactant_1_eq',
           'Reactant_1_mmol', 'Reactant_2_Name', 'Reactant_2_eq',
           'Catalyst_1_Short_Hand', 'Catalyst_1_eq', 'Ligand_Short_Hand',
           'Ligand_eq', 'Reagent_1_Short_Hand', 'Reagent_1_eq',
           'Solvent_1_Short_Hand', 'Product_Yield_PCT_Area_UV',
           'Product_Yield_Mass_Ion_Count']
        """
        continuous_params = [
            'Reagent_1_eq',
            'Reactant_1_mmol',
            'Catalyst_1_eq',
            'Ligand_eq',
        ]
        categorical_params = [
            'Reactant_1_Name',
            'Reactant_2_Name',
            'Catalyst_1_Short_Hand',
            'Ligand_Short_Hand',
            'Reagent_1_Short_Hand',
            'Solvent_1_Short_Hand',
        ]
        targets = ['Product_Yield_PCT_Area_UV', 'Product_Yield_Mass_Ion_Count']
        return BenchmarkDataframe('Suzuki-Miyaura coupling', source, continuous_params, categorical_params, targets, df)

    @classmethod
    def ds_1(cls, filename: FilePath = 'ds-1.csv'):
        source = f"{download_dir}/{filename}"
        df = pd.read_csv(source)
        """
        [
        'plate', 'row', 'col', 'base', 'base_cas_number', 'base_smiles',
           'ligand', 'ligand_cas_number', 'ligand_smiles', 'aryl_halide_number',
           'aryl_halide', 'aryl_halide_smiles', 'additive_number', 'additive',
           'additive_smiles', 'product_smiles', 'yield'
           ]
        """
        continuous_params = [
        ]
        categorical_params = [
            'base',
            'ligand_smiles',
            'aryl_halide',
            'additive',
            'product_smiles',
        ]
        # params = [
        #     'plate',
        #     'row',
        #     'col',
        # ]
        targets = [
            'YIELD'
        ]
        df.rename(columns={'yield': 'YIELD'}, inplace=True)
        return BenchmarkDataframe('Buchwald-Hartwig cross-coupling', source, continuous_params, categorical_params,
                                  targets, df)

    @classmethod
    def from_ord_pbgz(cls, filename: FilePath = 'ds-2.pb.gz'):
        source = f"{download_dir}/{filename}"
        dataset = load_message(source, Dataset)
        df = messages_to_dataframe(dataset.reactions)
        to_drop = []
        to_rename = {}
        for c in df.columns:
            if len(set(df[c].tolist())) == 1:
                to_drop.append(c)
            elif "vendor" in c:
                to_drop.append(c)
            elif "provenance" in c:
                to_drop.append(c)
            elif "preparations" in c:
                to_drop.append(c)
            elif "reaction_id" == c:
                to_drop.append(c)
            to_rename[c] = c.replace(" ", "_")
        df.drop(columns=to_drop, inplace=True)
        df.rename(columns=to_rename, inplace=True)
        columns = df.columns.tolist()
        continuous_columns =  df.select_dtypes(include=np.number).columns.tolist()
        targets = [c for c in continuous_columns if "outcome" in c]  # better double check
        params = [c for c in columns if c not in targets and "outcome" not in c]

        continuous_variables = [c for c in params if c in continuous_columns]
        categorical_variables = [c for c in params if c not in continuous_variables]
        return BenchmarkDataframe(dataset.dataset_id, source, continuous_variables, categorical_variables, targets, df)

    @classmethod
    def ds_2(cls, filename: FilePath = 'ds-2.pb.gz'):
        return BenchmarkDataframe.from_ord_pbgz(filename)

    @classmethod
    def ds_3(cls, filename: FilePath = 'ds-3.pb.gz'):
        return BenchmarkDataframe.from_ord_pbgz(filename)

    @classmethod
    def ds_4(cls, filename: FilePath = 'ds-4.pb.gz'):
        return BenchmarkDataframe.from_ord_pbgz(filename)


def load_benchmark_dataframes() -> list[BenchmarkDataframe]:
    logger.warning("loading benchmark dataframes")
    bds = [
        BenchmarkDataframe.ds_0(),
        BenchmarkDataframe.ds_1(),
        BenchmarkDataframe.ds_2(),
        BenchmarkDataframe.ds_3(),
        BenchmarkDataframe.ds_4(),
    ]
    logger.warning("loaded!")
    return bds
