#!/bin/sh

# ===========================================================
# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/dists/Linux/Attic/net_install-gnumed_client.sh,v $
# $Id: net_install-gnumed_client.sh,v 1.1 2008-02-21 16:22:06 ncq Exp $
# ===========================================================

VER_LATEST="CVS-HEAD"
INSTALL_BASE=~/".gnumed/client-installation"

# ===========================================================
VER_CLI="$1"
DL_BASE_URL="http://www.gnumed.de/downloads/client/0.2"		# FIXME: derive "0.2" from version
SYS_TYPE="generic Un*x"
PKG_INSTALLER=`which true`
DEPS=""

# determine version to install
if test -z ${VER_CLI} ; then
	TARGET_VER=${VER_LATEST}
else
	TARGET_VER=${VER_CLI}
fi ;

TGZ_NAME="GNUmed-client.${TARGET_VER}.tgz"
LAUNCHER=~/"Desktop/GNUmed ${TARGET_VER}"

# try to determine distribution of target system
# SuSE
if [ -f /etc/SuSE-release ]; then
	DEPS="postgresql tar coreutils mc python-psycopg2 openssl wget gzip file"
	PKG_INSTALLER="zypper install"
	SYS_TYPE="SuSE"
fi
# Debian
if [ -f /etc/debian_version ]; then
	DEPS="postgresql-client tar coreutils mc python-psycopg2 openssl wget gzip file python-gnuplot konsolekalendar aspell python python-enchant python-support python-wxgtk2.6"
	PKG_INSTALLER="apt-get install"
	SYS_TYPE="Debian"
fi
# Mandriva
if [ -f /etc/mandriva-release ]; then
	DEPS="postgresql-client tar coreutils mc python-psycopg2 openssl wget gzip file"
	PKG_INSTALLER="urpmi"
	SYS_TYPE="Mandriva"
fi

echo ""
echo "======================================================="
echo "This GNUmed helper will download and install the GNUmed"
echo "client v${TARGET_VER} onto your ${SYS_TYPE} machine. The system"
echo "account \"${USER}\" will be the only one able to use it."
echo ""
echo "It can also try to take care of installing any"
echo "dependancies needed to operate GNUmed smoothly."
echo ""
echo "A link will be put on the desktop so you can"
echo "easily start this version of the GNUmed client."
echo ""
echo "Installation directory:"
echo ""
echo "  ${INSTALL_BASE}/GNUmed-${TARGET_VER}/"
echo "======================================================="


# install dependancies
echo ""
echo "Installing dependancies ..."
echo ""
echo "Do you want to install the following dependancies"
echo "needed to smoothly operate the GNUmed client ?"
echo ""
echo "${DEPS}"
echo ""
read -e -p "Install dependancies ? [y/N]: "
if test "${REPLY}" == "y" ; then
	echo ""
	echo "You may need to enter the password for \"${USER}\" now:"
	sudo ${PKG_INSTALLER} ${DEPS}
fi


# prepare environment
mkdir -p ${INSTALL_BASE}
cd ${INSTALL_BASE}


# get and unpack package
echo ""
echo "Downloading ..."
wget -c "${DL_BASE_URL}/${TGZ_NAME}"
if test $? -ne 0 ; then
	echo "ERROR: cannot download v${TARGET_VER}, aborting"
	exit 1
fi
if test -d GNUmed-${TARGET_VER}/ ; then
	echo "It seems the client version v${TARGET_VER} is"
	echo "already installed. What do you want to do ?"
	echo ""
	echo " o - overwrite with new installation"
	echo " c - configure existing installation"
	echo " q - quit"
	echo ""
	read -e -p "Do what ? [o/c/q]: "
else
	REPLY="o"
fi
if test "${REPLY}" == "q" ; then
	exit 0
fi
if test "${REPLY}" == "c" ; then
	CONFIGURE="true"
elif test "${REPLY}" == "o" ; then
	rm -rf GNUmed-${TARGET_VER}/
	tar -xzf ${TGZ_NAME}
	if test $? -ne 0 ; then
		echo "ERROR: cannot unpack ${TGZ_NAME}, aborting"
		exit 1
	fi
	CONFIGURE="false"
else
	echo "ERROR: invalid choice: ${REPLY}"
	exit 1
fi


# check for dependancies
echo ""
echo "Checking dependancies ..."
cd GNUmed-${TARGET_VER}/client/
./check-prerequisites.sh


# activate local translation
cd locale/
# DE
mkdir -p ./de_DE/LC_MESSAGES/
cd de_DE/LC_MESSAGES/
ln -sf ../../de-gnumed.mo gnumed.mo
cd ../../
# ES
mkdir -p ./es_ES/LC_MESSAGES/
cd es_ES/LC_MESSAGES/
ln -sf ../../es-gnumed.mo gnumed.mo
cd ../../
# FR
mkdir -p ./fr_FR/LC_MESSAGES/
cd fr_FR/LC_MESSAGES/
ln -sf ../../fr-gnumed.mo gnumed.mo
cd ../../
# IT
mkdir -p ./it_IT/LC_MESSAGES/
cd it_IT/LC_MESSAGES/
ln -sf ../../it-gnumed.mo gnumed.mo
cd ../../../


# add desktop link
if test -e "${LAUNCHER}" ; then
	if test "${CONFIGURE}" == "true" ; then
		echo ""
		read -p "Editing launcher script (hit [ENTER]) ..."
		mc -e "${LAUNCHER}"
	else
		echo "#!/bin/sh" > "${LAUNCHER}"
		echo "" >> "${LAUNCHER}"
		echo "cd ${INSTALL_BASE}/GNUmed-${TARGET_VER}/client/" >> "${LAUNCHER}"
		echo "./gm-from-cvs.sh" >> "${LAUNCHER}"
	fi
else
	echo "#!/bin/sh" > "${LAUNCHER}"
	echo "" >> "${LAUNCHER}"
	echo "cd ${INSTALL_BASE}/GNUmed-${TARGET_VER}/client/" >> "${LAUNCHER}"
	echo "./gm-from-cvs.sh" >> "${LAUNCHER}"
fi
chmod u+x "${LAUNCHER}"


# edit config file
echo ""
read -p "Editing configuration file (hit [ENTER]) ..."
mc -e gm-from-cvs.conf

# ============================================
# $Log: net_install-gnumed_client.sh,v $
# Revision 1.1  2008-02-21 16:22:06  ncq
# - newly added
#
#