const calcTime = (timestamp) => {
    const curTime = new Date().getTime() - 9 * 60 * 60 * 1000;
    const time = new Date(curTime - timestamp); 
    const hour = time.getHours();
    const minute = time.getMinutes(); 
    const second = time.getSeconds(); 

    if (hour > 0) return `${hour} 시간 전`;
    else if (minute > 0) return `${minute}분 전`;
    else if (second >= 0) return `${seco