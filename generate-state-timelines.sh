#! /usr/bin/env bash

#--------[ Colors ]------------------------------------------------------------
Green='\033[0;32m'
Red='\033[0;31m'
Blue='\033[0;34m'
BBlue='\033[1;34m'
BWhite='\033[1;37m'
NC='\033[m'

#--------[ States ]------------------------------------------------------------

STATES=('AL' 'AK' 'AZ' 'AR' 'CA' 'CO' 'CT' 'DE' 'FL' 'GA' 'HI' 'ID' 'IL' 'IN' 
        'IA' 'KS' 'KY' 'LA' 'ME' 'MD' 'MA' 'MI' 'MN' 'MS' 'MO' 'MT' 'NE' 'NV'
        'NH' 'NJ' 'NM' 'NY' 'NC' 'ND' 'OH' 'OK' 'OR' 'PA' 'RI' 'SC' 'SD' 'TN'
        'TX' 'UT' 'VT' 'VA' 'WA' 'WV' 'WI' 'WY' )

#--------[ generate_state_timeline ]-------------------------------------------
function generate_state_timeline()
{
    echo -ne "    ${NC}[ ] $1${NC}"
    python plot-data.py $1 --save &> /dev/null
    retval=$?
    if (( $retval != 0 ));then
        echo -e "\r    ${Red}[X]${NC} "
    else
        echo -e "\r    ${Green}[*]${NC} "
    fi
}

#--------[ Main ]--------------------------------------------------------------
echo '+=========================================+'
echo '|    Generate All State COVID Timelines   |'
echo '+=========================================+'

SAVE_COMMAND="python plot-data.py <State> --save"
LOCATION="State-Timelines/"

echo -e "${Blue}[i]${NC} ${White}Command:  $SAVE_COMMAND${NC}"
echo -e "${Blue}[i]${NC} ${White}Location: $LOCATION${NC}"
echo -e "${Blue}[i]${NC} ${White}Be sure virtual env is active!${NC}"
echo
echo -e "${BBlue}[i]${NC} ${BWhite}Generating state timelines${NC}"

for s in ${STATES[@]}; do 
    generate_state_timeline $s
done
