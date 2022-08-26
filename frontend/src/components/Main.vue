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
      p1_width: '',
      p2_width: '',
      API_URL: 'http://localhost:8012/api/process'
    };
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
              var percent = 0;
              var finished = false;
              var i = 0;
              while (!finished) {
                  console.log(id, finished, percent);
                  sleep(200);
                  await fetch(this.API_URL + '?id=' + id)
                      .then(function(response) {
                          if (response.status != 200) {
                              finished = true;
                              throw response.status;
                          } else {
                              return response.json();
                          }
                      }.bind(this))
                      .then(function(data) {
                          console.log(data);
                          var percent = data['percent'];
                          if (id == 'b1') {
                              this.p1_width = percent + '%';
                          } else if (id == 'b2') {
                              this.p2_width = percent + '%';
                          };
                          if (percent >= 100) {
                              console.log("hihi")
                              finished = true;
                          }

                      }.bind(this))
                      .catch(function(error) {
                          console.log(error);
                          finished = true;
                          if (id == 'b1') {
                              this.p1_width = error
                          } else if (id == 'b2') {
                              this.p2_width = error
                          };

                      }.bind(this));
                  i = i + 1;
                  if (i > 1000) {
                      finished = true;
                  } // max 1000 iterations wait

              }

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