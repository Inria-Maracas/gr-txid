#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
from argparse import ArgumentParser

DEFAULT_TX_GAIN = 8
RX_GAIN = 25
NUM_NODES = 40

parser = ArgumentParser()
parser.add_argument(
    "-i",
    dest="docker_img",
    type=str,
    default="",
    help="Docker image to run",
    required=True,
)
parser.add_argument(
    "-d",
    dest="exp_duration",
    help="Single experiment duration (s)",
    type=int,
    default=60,
)
parser.add_argument(
    "-t",
    "--tx_nodes",
    help="List of transmitting nodes",
    type=lambda s: [int(item) for item in s.split(",")],
    required=True,
)
parser.add_argument(
    "-g",
    "--tx_nodes_gains",
    help="List of transmitting nodes gains",
    type=lambda s: [int(item) for item in s.split(",")],
)
parser.add_argument(
    "-r",
    "--rx_nodes",
    help="List of recieving nodes",
    type=lambda s: [int(item) for item in s.split(",")],
    default=[1000],
)
parser.add_argument(
    "-G",
    "--rx-gain",
    dest="rx_gain",
    type=float,
    default=float(25),
    help="Set Reciever gain [default=%(default)r]",
)
parser.add_argument(
    "-a",
    "--samp-rate",
    dest="samp_rate",
    type=int,
    default=5000000,
    help="Set Sample rate [default=%(default)r]",
)
parser.add_argument(
    "-b",
    "--filter-width",
    dest="filter_width",
    type=float,
    default=float(0),
    help="Set Tx Filter Bandwidth [default=%(default)r]",
)
parser.add_argument(
    "-f",
    "--center-freq",
    dest="center_freq",
    type=float,
    default=float(433e6),
    help="Set Center frequency [default=%(default)r]",
)
parser.add_argument("-s", dest="sched_node", help="Scheduler node", type=int, default=2)
parser.add_argument(
    "--tx_freq", help="Frequency of new packet transmission", type=float, default=0.001
)
parser.add_argument(
    "--var_freq", help="Frequency of power variation", type=float, default=2
)
parser.add_argument(
    "-p",
    dest="port_num",
    help="Port to send scheduling paquets to",
    type=int,
    default=3580,
)
parser.add_argument(
    "-v",
    dest="is_var",
    help="Power variation transmission type? [default=%(default)r]",
    action="store_true",
)
parser.add_argument(
    "-R",
    dest="is_random",
    help="Use random modulated packets? [default=%(default)r]",
    action="store_true",
)
parser.add_argument(
    "-N",
    dest="is_noise",
    help="Use noise packets? [default=%(default)r] (Has priority over -r)",
    action="store_true",
)
args = parser.parse_args()

date = time.strftime("%Y%m%d_%Hh%M")

rx_nodes = args.rx_nodes
tx_nodes = args.tx_nodes
RX_GAIN = args.rx_gain
tx_nodes_gains = args.tx_nodes_gains
if tx_nodes_gains is None:
    tx_nodes_gains = []
for i in range(min(len(tx_nodes_gains), len(tx_nodes)), len(tx_nodes)):
    tx_nodes_gains.append(DEFAULT_TX_GAIN)
tx_node_string = ""
for tx_node in tx_nodes:
    tx_node_string += f"{tx_node},"
tx_node_string = tx_node_string[:-1]

pow_var_speed = args.var_freq

docker_img_string = args.docker_img

for rx_idx, rx in enumerate(rx_nodes):
    yaml_content = "description: Base scenario for TXid dataset generation\n\n\n"

    yaml_content += f"duration: {args.exp_duration}\n\n"
    yaml_content += "nodes:\n"

    for node_id in range(1, NUM_NODES):
        if node_id == rx:  # Write the command to launch RX on this node
            yaml_content += f"  node{node_id}:\n"
            yaml_content += "    container:\n"
            yaml_content += f"    - image: {docker_img_string}\n"
            yaml_content += f'      command: bash -lc "/root/gr-txid/examples/src/reciever.py -g {RX_GAIN} -T {len(tx_nodes)} -F enreg_{rx_idx:02d} -a {args.samp_rate} -c {args.center_freq} "\n\n'  # TODO Add num samples to save?
            continue

        if (
            node_id == args.sched_node
        ):  # TODO Allow scheduler to run on a Tx or Rx node?
            yaml_content += f"  node{node_id}:\n"
            yaml_content += "    container:\n"
            yaml_content += f"    - image: {docker_img_string}\n"
            yaml_content += f'      command: bash -lc "/root/gr-txid/examples/src/scheduler.py -p {args.port_num} -s {args.tx_freq} -n {tx_node_string}"\n'
            yaml_content += "    passive: true\n\n"
            continue

        if node_id in tx_nodes:
            tx_index = tx_nodes.index(node_id)
            yaml_content += f"  node{node_id}:\n"
            yaml_content += "    container:\n"
            yaml_content += f"    - image: {docker_img_string}\n"
            yaml_content += f'      command: bash -lc "/root/gr-txid/examples/src/emitter.py -P {args.port_num} -T {tx_nodes.index(node_id)} -a {args.samp_rate} -b {args.filter_width} -c {args.center_freq} -G {tx_nodes_gains[tx_index]} -R {int(args.is_random)} -r {int(args.is_noise)} -f {pow_var_speed * int(args.is_var)} -M 0.5"\n'
            yaml_content += "    passive: true\n\n"

    # Folder creation
    folder = "node" + str(rx) + "/"
    os.makedirs(folder, exist_ok=True)

    # Write new file
    new_file = folder + "scenario.yaml"
    fichier = open(new_file, "w")
    fichier.write(yaml_content)
    fichier.close()


print("Fin.")
