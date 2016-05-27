#!/bin/bash
clear
echo "`whoami`@$(hostname):${PWD}\$ test";

outResp(){
    echo ""
    echo ""
    echo "======================================================================";
    echo "=== $1";
    echo "======================================================================";
    if test -n "$3"; then
        echo " ";
        echo "[i] 准备执行指令:";
        echo "`whoami`@$(hostname):${PWD}\$ $2";
        echo " ";
        echo "                     <<< 按 Enter 键继续 >>>";
        echo "===-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-===";
    else
        echo "           ......>>> 正在处理指令,请稍候 >>>...... ";
        echo "`whoami`@$(hostname):${PWD}\$ $2";
    fi

    if test -z "$3"; then
        $2;
    else
        if "true" == "$3"; then
            read var;
            $2;
        else
            $2;
        fi
    fi
    echo "------------------------------------------------------------<DONE>----";
    echo ""
}

outResp "MWORKER SERVICE" "echo bash $0"

#find location by shell script directory
SOURCE="$0"
while [ -h "$SOURCE"  ]; do
    DIR="$( cd -P "$( dirname "$SOURCE"  )" && pwd  )";
    SOURCE="$(readlink "$SOURCE")";
    [[ $SOURCE != /*  ]] && SOURCE="$DIR/$SOURCE";
done

workspace="$( cd -P "$( dirname "$SOURCE"  )" && pwd  )";
outResp "切换工作目录到:${workspace}" "cd ${workspace}";

outResp "正在启动......" "python main/mService.py"

