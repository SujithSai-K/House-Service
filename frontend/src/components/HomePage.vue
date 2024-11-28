<template>
  <div >
    <div class="img" ><img src="@/assets/logo1.png" alt="" width="250" height="250"></div>
    <div>
    <router-link class="btn btn-primary mt-3" to="/login">Login</router-link>
    <router-link class="btn btn-secondary mt-3" to="/user_register" style="margin-left: 3px;">Register</router-link>
  </div>
  <div class="container mt-3">
    <h1>
        <span class="typed-text">{{ typeValue }}</span>
        <span class="cursor" :class="{'typing':typeStatus}">&nbsp;</span>
    </h1>
  </div>
  
  </div>
</template>

<script>
export default {
    name: 'HomePage',
    data: () =>{
        return{
            typeValue: '',
            typeStatus: 'false',
            typeArray: ['Welcome to HOUSE CARE', 'Please Login', 'To get your Service'],
            typingSpeed: 200,
            erasingSpeed: 100,
            newTextDelay: 2000,
            typeArrayIndex: 0,
            charIndex: 0,
        }
    },
    methods: {
        typeText(){
            if(this.charIndex < this.typeArray[this.typeArrayIndex].length){
                if(!this.typeStatus){
                    this.typeStatus = 'true';
                }
                this.typeValue += this.typeArray[this.typeArrayIndex].charAt(this.charIndex);
                this.charIndex += 1;

                setTimeout(this.typeText, this.typingSpeed);
            }
            else{
                this.typeStatus = 'flase';
                setTimeout(this.eraseText, this.newTextDelay);
            }
        },
        eraseText(){
            if(this.charIndex>0){
                if(!this.typeStatus){
                    this.typeStatus = 'true';
                }
                this.typeValue = this.typeArray[this.typeArrayIndex].substring(0,this.charIndex -1);
                this.charIndex -= 1 ;
                setTimeout(this.eraseText, this.erasingSpeed)
            }
            else{
                this.typeStatus = 'false';
                this.typeArrayIndex += 1;
                if(this.typeArrayIndex >= this.typeArray.length)
                    this.typeArrayIndex = 0
                setTimeout(this.typeText, this.typingSpeed + 1000)
            }

        }
    },
    created(){
        setTimeout(this.typeText, this.newTextDelay+200);
    }
}
</script>

<style scoped>
    .img{
        margin-top: 6%;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .container{
        /* width: 100vw;
        height: 100vh; */
        display: flex;
        justify-content: center;
        align-items: center;
    }
    h1{
        font-size: 4rem;
        font-weight: normal;

        span.typed-text{
            color: #000000;
        }

        span.cursor{
            display: inline-block;
            margin-left: 3px;
            width: 4px;
            background-color: #000000;
            animation:cursorBlink 1s infinite;
        }
        span.cursor.typing{
            animation: none;
        }
    }

    @keyframes cursorBlink {
        49%{background-color: #000000;} 
        50%{background-color: white;}
        99%{background-color: white;}       
    }
</style>>
