console.log('let\'s write javascript');
async function main(){
    let a= fetch("http://127.0.0.1:5500/songs/")
    let response = await a.read();
    console.log(response);
}
main()
