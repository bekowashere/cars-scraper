import json

json_files = ['all_specification_types_ac.json', 'all_specification_types_acura.json', 'all_specification_types_alfaromeo.json', 'all_specification_types_alpine.json', 'all_specification_types_ariel.json', 'all_specification_types_aro.json', 'all_specification_types_artega.json', 'all_specification_types_astonmartin.json', 'all_specification_types_audi.json', 'all_specification_types_aurus.json', 'all_specification_types_bentley.json', 'all_specification_types_bmw.json', 'all_specification_types_bristol.json', 'all_specification_types_bufori.json', 'all_specification_types_bugatti.json', 'all_specification_types_buick.json', 'all_specification_types_cadillac.json', 'all_specification_types_caterham.json', 'all_specification_types_chevrolet.json', 'all_specification_types_chrysler.json', 'all_specification_types_citroen.json', 'all_specification_types_cupra.json', 'all_specification_types_dacia.json', 'all_specification_types_daewoo.json', 'all_specification_types_daihatsu.json', 'all_specification_types_datsun.json', 'all_specification_types_delorean.json', 'all_specification_types_dodge.json', 'all_specification_types_donkervoort.json', 'all_specification_types_drmotor.json', 'all_specification_types_dsautomobiles.json', 'all_specification_types_eagle.json', 'all_specification_types_ferrari.json', 'all_specification_types_fiat.json', 'all_specification_types_fisker.json', 'all_specification_types_ford.json', 'all_specification_types_fso.json', 'all_specification_types_geely.json', 'all_specification_types_genesis.json', 'all_specification_types_gmc.json', 'all_specification_types_gtamotor.json', 'all_specification_types_hindustan.json', 'all_specification_types_holden.json', 'all_specification_types_honda.json', 'all_specification_types_hummer.json', 'all_specification_types_hyundai.json', 'all_specification_types_infiniti.json', 'all_specification_types_isuzu.json', 'all_specification_types_jaguar.json']


def merge_json_types(filename):
    result = list()
    for f1 in filename:
        with open(f1, 'r') as f:
            data = json.load(f)
            for obj in data:
                if not obj in result:
                    result.append(obj)

        with open('merge_types.json', 'w') as f:
            json.dump(result, f, indent=2)

merge_json_types(json_files)