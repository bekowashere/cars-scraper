import json


json_files = ['all_specifications_ac.json', 'all_specifications_acura.json', 'all_specifications_alfaromeo.json', 'all_specifications_alpine.json', 'all_specifications_ariel.json', 'all_specifications_aro.json', 'all_specifications_artega.json', 'all_specifications_astonmartin.json', 'all_specifications_audi.json', 'all_specifications_aurus.json', 'all_specifications_bentley.json', 'all_specifications_bmw.json', 'all_specifications_bristol.json', 'all_specifications_bufori.json', 'all_specifications_bugatti.json', 'all_specifications_buick.json', 'all_specifications_cadillac.json', 'all_specifications_caterham.json', 'all_specifications_chevrolet.json', 'all_specifications_chrysler.json', 'all_specifications_citroen.json', 'all_specifications_cupra.json', 'all_specifications_dacia.json', 'all_specifications_daewoo.json', 'all_specifications_daihatsu.json', 'all_specifications_datsun.json', 'all_specifications_delorean.json', 'all_specifications_dodge.json', 'all_specifications_donkervoort.json', 'all_specifications_drmotor.json', 'all_specifications_dsautomobiles.json', 'all_specifications_eagle.json', 'all_specifications_ferrari.json', 'all_specifications_fiat.json', 'all_specifications_fisker.json', 'all_specifications_ford.json', 'all_specifications_fso.json', 'all_specifications_geely.json', 'all_specifications_genesis.json', 'all_specifications_gmc.json', 'all_specifications_gtamotor.json', 'all_specifications_hindustan.json', 'all_specifications_holden.json', 'all_specifications_honda.json', 'all_specifications_hummer.json', 'all_specifications_hyundai.json', 'all_specifications_infiniti.json', 'all_specifications_isuzu.json', 'all_specifications_jaguar.json']

def merge_JsonFiles(filename):
    result = list()
    for f1 in filename:
        with open(f1, 'r') as f:
            data = json.load(f)
            for obj in data:
                if not obj in result:
                    result.append(obj)

        with open('merge_specifications.json', 'w') as f:
            json.dump(result, f, indent=2)

merge_JsonFiles(json_files)