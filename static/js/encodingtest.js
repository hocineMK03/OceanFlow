var inputdata="";
var concat="";
var tabbin=[];
var tabdec=[];







function converting(which){

    if(which==1){
        for(let i=0;i<inputdata.length;i++){
            let tmp=inputdata.charAt(i).charCodeAt(0);
        
        
        
         
         tabbin[i]=convertto8bits(tmp.toString());
        }
        concat=tabbin.join("");
         
    }
    else if(which==2){
       
        let len=concat.length;
       
        for(let i=0;i<len;i=i+6){
            
            let tmp1=concat.slice(i,i+6);
            
            
            
             tabdec[i]=converttodecimal(tmp1.toString());
            

        }
        concat=tabdec.join("");
        
    }
    


}
function convertto8bits(variable1){


let con="";

variable1=Number(variable1);

 let len=variable1.toString(2).length;

for(let i=0;i<8-len;i++){
    con+="0";
    
}
con+=variable1.toString(2);

return con;

}


function converttodecimal(variable1){
    let con="";
    let tmp=variable1;
    
    let len=variable1.toString().length;
    
    if (len === 2) {
        tmp+="0000";
       
      } else if (len === 4) {
        tmp+="00";
      }
variable1=tmp;

//change if wrong

variable1=Number.parseInt(variable1,2);
console.log("var",variable1);
if(variable1>=0 && variable1<=25){
    variable1=variable1+65;
}
else if(variable1>=26 && variable1<=51){
    variable1=variable1+71;
}

else if(variable1>=52 && variable1<=61){
    variable1=variable1-4;
    
}
else if(variable1==62){
    variable1=variable1-19;
}else if(variable1==63){
    variable1=variable1-16;
}



con=variable1;
let fin=String.fromCharCode(con);
con=fin.toString();

if (len === 2) {
    con += "==";
  } 
  else if (len === 4) {
    con += "=";
  }

return con;
}


function init1(inputdata1){
inputdata=inputdata1;
converting(1);
converting(2);

return concat;
}



