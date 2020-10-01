#!/bin/sh

NETDATA_PLUGINS_DIR="/usr/libexec/netdata/python.d"
NETDATA_CONFIG_DIR="/etc/netdata"
INSTALL_ALARMS=true
PLUGIN_FILE="monerod.chart.py"
CONFIG_FILE="monerod.conf"
ALARMS_FILE="health.d/monerod.conf"

usage()
{
    echo "monerod netdata plugin - installation script"
    echo ""
    echo "$0"
    echo "  -h --help"
    echo "  --plugins-dir=path          Default python.d plugins directory: $NETDATA_PLUGINS_DIR"
    echo "  --config-dir=path           Default netdata configuration directory: $NETDATA_CONFIG_DIR"
    echo "  --without-alarms            Add this option to install only plugin (skip netdata alarms installation)"
    echo ""
}

#parse arguments
while [ "$1" != "" ]; do
    PARAM=`echo $1 | awk -F= '{print $1}'`
    VALUE=`echo $1 | awk -F= '{print $2}'`
    case $PARAM in
        -h | --help)
            usage
            exit
            ;;
        --plugins-dir)
            NETDATA_PLUGINS_DIR=$VALUE
            ;;
        --config-dir)
            NETDATA_CONFIG_DIR=$VALUE
            ;;
        --without-alarms)
            INSTALL_ALARMS=false
            ;;
        *)
            echo "ERROR: unknown parameter \"$PARAM\""
            usage
            exit 1
            ;;
    esac
    shift
done

#remove trailing '/ to directories...
NETDATA_PLUGINS_DIR="${NETDATA_PLUGINS_DIR%/}"
NETDATA_CONFIG_DIR="${NETDATA_CONFIG_DIR%/}"

#check if plugins and config directories exist
if [ ! -d $NETDATA_PLUGINS_DIR ]; then
    echo "'$NETDATA_PLUGINS_DIR' does not exist, you can specify netdata python.d plugins directory with '--plugins-dir=path' option."
    exit 1
fi
if [ ! -d $NETDATA_CONFIG_DIR ]; then
    echo "'$NETDATA_CONFIG_DIR' does not exist, you can specify netdata configuration directory with '--config-dir=path' option."
    exit 1
fi

#copy files
yes | cp -rf $PLUGIN_FILE $NETDATA_PLUGINS_DIR/$PLUGIN_FILE
if [ $? -ne 0 ]; then
    echo "Error while copying $PLUGIN_FILE file."
    exit 1
fi
echo "ok: $PLUGIN_FILE was copied to $NETDATA_PLUGINS_DIR/$PLUGIN_FILE"
yes | cp -rf $CONFIG_FILE $NETDATA_CONFIG_DIR/python.d/$CONFIG_FILE
if [ $? -ne 0 ]; then
    echo "Error while copying $CONFIG_FILE file."
    exit 1
fi
echo "ok: $CONFIG_FILE was copied to $NETDATA_CONFIG_DIR/python.d/$CONFIG_FILE"
if [ "$INSTALL_ALARMS" = true ] ; then
    yes | cp -rf $ALARMS_FILE $NETDATA_CONFIG_DIR/$ALARMS_FILE
    if [ $? -ne 0 ]; then
        echo "Error while copying $ALARMS_FILE file."
        exit 1
    fi
    echo "ok: $ALARMS_FILE was copied to $NETDATA_CONFIG_DIR/$ALARMS_FILE"
    chown netdata:netdata $NETDATA_CONFIG_DIR/$ALARMS_FILE
fi
chown netdata:netdata $NETDATA_PLUGINS_DIR/$PLUGIN_FILE
chown netdata:netdata $NETDATA_CONFIG_DIR/python.d/$CONFIG_FILE

exit 0
