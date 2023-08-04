var inputdata1="";
var concat1="";
var tabbin1=[];
var tabdec1=[];







function converting1(which){

    if(which==1){
        for(let i=0;i<inputdata1.length;i++){
            
                let tmp=inputdata1.charAt(i).charCodeAt(0);
        
        
        
         
                tabbin1[i]=convertto8bits1(tmp.toString());
            
            
        }
        concat1=tabbin1.join("");
        console.log("first",concat1.length,concat1);        
    }
    else if(which==2){
       
        let len=concat1.length;
        console.log(concat1);
        for(let i=0;i<len;i=i+8){
            
            let tmp1=concat1.slice(i,i+8);
            
            
            
             tabdec1[i]=converttodecimal1(tmp1.toString());
            

        }
        concat1=tabdec1.join("");
        console.log("second",concat1.length,concat1); 
    }



}
function convertto8bits1(variable1){


let con="";



if(variable1!=61){
  

    
    console.log("var",variable1);
    variable1=Number(variable1);
    if(variable1>=97 && variable1<=122){
        variable1=variable1-71;
    }
    else if(variable1>=65 && variable1<=90){
        variable1=variable1-65;
    }
    
    else if(variable1>=48 && variable1<=57){
        variable1=variable1+4;
    }
    else if(variable1==43){
        variable1=variable1+19;
    }else if(variable1==47){
        variable1=variable1+16;
    }
    console.log("var1",variable1);
 let len=variable1.toString(2).length;
 for(let i=0;i<6-len;i++){
    con+="0";
    
}
con+=variable1.toString(2);

return con;
}

   


    return con;





}


function converttodecimal1(variable1){
    let con="";
    let len=variable1.toString().length;
    

variable1=Number.parseInt(variable1,2);





con=variable1;
let fin=String.fromCharCode(con);
con=fin;
console.log(variable1,con);
return con;
}
function init(inputdata2){
    inputdata1=inputdata2;
converting1(1);
converting1(2);

return concat1;
}






