import argparse

from easy_tpp.config_factory import Config
from easy_tpp.runner import Runner


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--config_dir', type=str, required=False, default='configs/experiment_config.yaml',
                        help='Dir of configuration yaml to train and evaluate the model.')

    parser.add_argument('--experiment_id', type=str, required=False, default='AttNHP_train',
                        help='Experiment id in the config file.')

    #parser.add_argument('--dataset', type=str, required=False, default='so', help='dataset name') 
    parser.add_argument('--seed', type=int, required=False, default=2015, help='Random seed number')

    args = parser.parse_args()

    config = Config.build_from_yaml_file(args.config_dir, experiment_id=args.experiment_id, seed=args.seed)


    model_runner = Runner.build_from_config(config)

    model_runner.run()


if __name__ == '__main__':
    main()
