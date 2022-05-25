<template>
    <v-main>
        <v-data-table
            :headers="headers"
            :items="desserts"
            :items-per-page="5"
            class="elevation-1"
        ></v-data-table>
  </v-main>
</template>

<script>
  export default {
    props: ["duct"],
    data () {
      return {
        headers: [
          {
            text: 'KEY',
            align: 'start',
            value: 'key',
          },
          { text: 'VALUE', value: 'value' },
          { text: 'TYPE', value: 'type' },
          { text: 'TTL', value: 'ttl' },
          //{ text: 'LEN', value: 'protein' },
          //{ text: 'MEMBER', value: 'iron' },
        ],
        desserts: [
          {
            key: 'Data/UserId:{id}',
            value: 159,
            type: 6.0,
            ttl: 24,
            protein: 4.0,
            iron: '1%',
          },
          {
            key: 'Data/UserId:{id}',
            value: 237,
            type: 9.0,
            ttl: 37,
            protein: 4.3,
            iron: '1%',
          },
          {
            key: 'Data/UserId:{id}',
            value: 262,
            type: 16.0,
            ttl: 23,
            protein: 6.0,
            iron: '7%',
          },
          {
            key: 'Data/UserId:{id}',
            value: 305,
            type: 3.7,
            ttl: 67,
            protein: 4.3,
            iron: '8%',
          },
          {
            key: 'Data/UserId:{id}',
            value: 356,
            type: 16.0,
            ttl: 49,
            protein: 3.9,
            iron: '16%',
          },
          {
            key: 'Data/UserId:{id}',
            value: 375,
            type: 0.0,
            ttl: 94,
            protein: 0.0,
            iron: '0%',
          },
          {
            key: 'Data/UserId:{id}',
            value: 392,
            type: 0.2,
            ttl: 98,
            protein: 0,
            iron: '2%',
          },
          {
            key: 'Data/UserId:{id}',
            value: 408,
            type: 3.2,
            ttl: 87,
            protein: 6.5,
            iron: '45%',
          },
          {
            key: 'Data/UserId:{id}',
            value: 452,
            type: 25.0,
            ttl: 51,
            protein: 4.9,
            iron: '22%',
          },
          {
            key: 'Data/UserId:{id}',
            value: 518,
            type: 26.0,
            ttl: 65,
            protein: 7,
            iron: '6%',
          },
        ],
      }
    },
    created: function() {
        console.log("hello!!!");
        this.duct.invokeOrWaitForOpen(() => {
            this.duct.eventListeners.resource.on("getRedisTable", {
                success: (data) => {
                    console.log(data);
                    let table = [];
                    for(let i in data["RedisData"]) {
                        let row = {};
                        row["key"] = data["RedisData"][i]["KEY"];
                        row["type"] = data["RedisData"][i]["TYPE"];
                        row["value"] = data["RedisData"][i]["VALUE"];
                        row["ttl"] = data["RedisData"][i]["TTL"];
                        table.push(row);
                    }
                    this.desserts = table;
                },
                error: (data) => {
                    console.log(data);
                }
            });
        });
        this.duct.controllers.resource.getRedisTable();
    }
  }
</script>