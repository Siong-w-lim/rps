#!/usr/bin/env python

import visa
import argparse

rm=0 #VISA resource manager
ps=0 #power supply instance

def check_inst():
    global ps
    x = ps.query('*IDN?')
    print(x)
    y = x.split(", ")
    if y[0] != "Keithley instruments" or y[1] != "2231A-30-3":
        disconnect()
        raise Exception("This is not Keithley 2231A")

def connect(dev):
    global rm, ps
    rm = visa.ResourceManager()
    #print rm.list_resources()
    dev = 'ASRL' + dev + '::INSTR'
    ps = rm.open_resource(dev, baud_rate=9600, data_bits=8)
    ps.write_termination = '\n'
    ps.read_termination = '\n'
    ps.write('SYST:REM') #Enable remote Contol

def disconnect():
    global rm, ps
    ps.write("SYST:LOC")
    ps.close
    rm.close

def channel(ch):
    global ps
    print("Selected channel %s" % ch)
    ps.write("INST:NSEL %s" % ch)

def voltage(volt):
    global ps
    print("Set voltage %f" % volt)
    ps.write("VOLT %f" % volt)

def current(amp):
    global ps
    print("Set current %f" % amp)
    ps.write("CURR %f" % amp)

def output(onoff):
    global ps
    print("Set output %s" % onoff)
    ps.write("OUTP %s" % onoff)

def info():
    x = ps.query("OUTP?")
    print ("Output: %s" % x)
    x = ps.query("VOLT?")
    y = ps.query("MEAS:VOLT?")
    print ("Voltage: %s/%sV" % (y,x))
    x = ps.query("CURR?")
    y = ps.query("MEAS:CURR?")
    print ("Current: %s/%sA" % (y,x))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--channel", help="Select Channel", choices=["1", "2", "3"], required=True)
    parser.add_argument("-v", "--voltage", help="Set Voltage", type=float)
    parser.add_argument("-a", "--ampere", help="Set Current limit", type=float)
    parser.add_argument("-o", "--output", help="Output on/off", choices=["0", "1"])
    parser.add_argument("-d", "--device", help="Device Path", default="/dev/ttyUSB0")
    parser.add_argument("-i", "--info", help="Get Channel Info", action='store_true')
    args = parser.parse_args()
    #print args
    connect(args.device)
    check_inst()
    channel(args.channel)

    if args.voltage is not None:
        voltage(args.voltage)
    if args.ampere is not None:
        current(args.ampere)
    if args.output is not None:
        output(args.output)
    if args.info is True:
        info()

    disconnect()
