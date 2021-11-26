<template>
<div>
  <div id="detail" class="height: 80%; weight: 80%"></div>
</div>
</template>

<script>
export default {
  name: 'Detail',
  data () {
    return {
      fiveDay: [
      ]
    }
  },
  created () {
    this.getData()
  },
  mounted () {
    document.getElementById('detail').style.height = window.screen.availHeight * 0.005 + 'px'
    this.$nextTick(() => {
      this.getData()
    })
    window.addEventListener('resize', () => {
      this.$echarts.init(document.getElementById('detail')).resize()
    })
  },

  methods: {
    getData () {
      let that = this
      // 发送特定日期的POST请求
      this.$axios
        .post('/detail', {name: that.$route.params.id}).then((Response) => {
          that.fiveDay = Response.data.data
          this.$options.methods.drawBar.bind(this)()
        })
        .catch((failResponse) => {
          console.log(failResponse)
        })
    },
    convertDate () {
      let res = []
      for (let i = 0; i < this.fiveDay.length; i++) {
        let date = this.fiveDay[i].date
        if (date) {
          res.push(date)
        }
      }
      console.log('date')
      console.log(res)
      console.log('date')
      return res
    },
    convertData (tmp) {
      let res = []
      for (let i = 0; i < this.fiveDay.length; i++) {
        let pm = this.fiveDay[i][tmp]
        if (pm) {
          res.push(pm)
        }
      }
      console.log(tmp)
      console.log(res)
      return res
    },
    drawBar () {
      let detailContainer = document.getElementById('detail')
      let resizeDetailContainer = function () {
        detailContainer.style.width = document.body.offsetWidth + 'px'
        detailContainer.style.height = window.screen.availHeight + 'px'
      }
      resizeDetailContainer()
      // 基于准备好的dom，初始化echarts实例
      let detail = this.$echarts.init(detailContainer)
      let optionMap = {
        title: {
          text: '折线图堆叠'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            label: {
              backgroundColor: '#6a7985'
            }
          }
        },
        legend: {
          data: ['AQI', 'PM2.5(μg/m³)', 'PM10(μg/m³)', 'SO₂(μg/m³)', 'O₃(μg/m³)', 'CO(mg/m³)', 'NO₂(μg/m³)']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        toolbox: {
          feature: {
            saveAsImage: {}
          }
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: this.convertDate()
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: 'AQI',
            type: 'line',
            data: this.convertData('aqi_24h')
          },
          {
            name: 'PM2.5(μg/m³)',
            type: 'line',
            data: this.convertData('pm2_5_24h')
          },
          {
            name: 'PM10(μg/m³)',
            type: 'line',
            data: this.convertData('pm10_24h')
          },
          {
            name: 'SO₂(μg/m³)',
            type: 'line',
            data: this.convertData('so2_24h')
          },
          {
            name: 'O₃(μg/m³)',
            type: 'line',
            data: this.convertData('o3_8h_24h')
          },
          {
            name: 'CO(mg/m³)',
            type: 'line',
            data: this.convertData('co_24h')
          },
          {
            name: 'NO₂(μg/m³)',
            type: 'line',
            data: this.convertData('no2_24h')
          }
        ]
      }
      detail.setOption(optionMap)
    }
  }
}
</script>

<style>

</style>
