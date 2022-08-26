<template>
  <div>
    <h1>VeriDeal Test</h1>
    <div class="row">
      <div class="Progress">
        <div id="p1" class="progressBar" :style="{ width: p1_width }"><b>{{p1_width}}</b></div>
      </div>
      <button id="b1"  @click="start">Start</button>
    </div>
    <div style="margin-top: 15px; margin-bottom: 15px;"></div>
    <div class="row">
      <div class="Progress">
        <div id="p2" class="progressBar" :style="{ width: p2_width }"><b>{{p2_width}}</b></div>
      </div>
      <button id="b2" @click="start">Start</button>
    </div>

  </div>
</template>

<script lang="ts">

function sleep(delay) {
    var start = new Date().getTime();
    while (new Date().getTime() < start + delay);
}

import {defineComponent} from 'vue';
export default defineComponent({
  name: 'Main',
  data() {
    return {
      socket: null,
      p1_width: '',
      p2_width: '',
      API_URL: 'http://localhost:8012/api/process',
      WS_URL: 'ws://localhost:8012/ws/process'
    };
  },
  created: function() {
    var _this = this;
    console.log("Starting connection to WebSocket Server")
    _this.socket = new WebSocket(_this.WS_URL);
    _this.socket.addEventListener('open', (event) => {
      //socket.send(JSON.stringify({id: 'b1'}));
    });

    
    _this.socket.addEventListener('message', function (event) {
      var event_data = JSON.parse(event.data);
      console.log('Data from server ', event_data);
      if(event_data.id == 'b1'){ 
        _this.p1_width = event_data.percent + '%';
      }else if(event_data.id == 'b2'){
        _this.p2_width = event_data.percent + '%';
      }
      
    });

  },
  methods: {
    async start_process(id) {
        return await fetch(this.API_URL, {
                method: 'POST',
                body: JSON.stringify({
                    'id': id
                })
            })
            .then(function(response) {
                if (response.status != 200) {
                    throw response.status;
                } else {
                    return response.json();
                }
            }.bind(this))
            .then(function(data) {
                console.log(data);
                return true;

            }.bind(this))
            .catch(function(error) {
                console.log(error);
                return false;
            }.bind(this));

    },
    async start(event) {
          var id = event.target.id;
          console.log("starting process..", id);
          var status = await this.start_process(id);
          //console.log(status);
          if (status) {
          } else {
              console.log("unable to start process.", id);
          }

      },
      stop() {
          console.log("stop");
          //this.progresses.pop()?.finish();
      },
  },
});
</script>


<style>
h3 {
  margin: 40px 0 0;
}
button {
  margin-right: 0.5rem;
}
button:last-child {
  margin-right: 0rem;
}

.Progress {
  width: 100%;
  background-color: black;
}

.progressBar {
  width: 0%;
  height: 40px;
  background-color: orange;
  text-align: center;
  line-height: 40px;
  color: white;
}
</style>