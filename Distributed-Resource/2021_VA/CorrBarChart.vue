<script>
import { HorizontalBar , mixins } from 'vue-chartjs'


export default {
    extends: HorizontalBar,
    mixins: [mixins.reactiveProp],
    props: ['chartData'],
    data: () => {return {
        type: 'horizontalBar',
        options: {
            responsive: true,
            maintainAspectRatio: true,
            legend:false,
            scales: {
                scales: {
                    xAxes: [{
                        ticks: {
                            min: 60, // Edit the value according to what you need
                            autoSkip: false,
                            maxRotation: 90,
                            minRotation: 90,
                            padding: -110
                        }
                    }],
                }
            },
    
            onClick: function(e) {
                var element = this.getElementAtEvent(e);

                console.log(element);
                console.log(this.data.datasets[0].hoverBorderColor);
                if (element.length===0)
                    return;

                if (this.data.datasets[0].clickedBarIndexes.includes(element[0]._index)) {
                    this.data.datasets[0].backgroundColor[element[0]._index]='rgba(204,204,204,0.7)';
                    this.data.datasets[0].clickedBarIndexes.splice(
                        this.data.datasets[0].clickedBarIndexes.indexOf(element[0]._index),1);
                }
                else{
                    this.data.datasets[0].backgroundColor[element[0]._index]='#ce1a26';
                    this.data.datasets[0].clickedBarIndexes.push(element[0]._index);
                }
                
                console.log(this.data.datasets[0].clickedBarIndexes);
                console.log(this.data.datasets[0].backgroundColor);
                // console.log(this);
                // element[0].$previousStyle.backgroundColor='rgb(255,0,0)'

                // for( var i=0; i< this.backgroundColor.length;i++) {
                //     this.backgroundColor[i] = 'rgb(1,1,1)';
                // }
                // console.log(element);
                // console.log(element[0]._index)
                // console.log(this.backgroundColor);
                    //this.backgroundColor[element[0]._index] = 'red';
                this.data.datasets[0].updateFeatureIdxs( this.data.datasets[0].clickedBarIndexes );
                this.update()
            }
        }
    }},
    methods:{
            handle () {
                
                console.log("asd");
                //const item = event[0]
            //     this.$emit('on-receive', {
            //     index: item._index,
            //     backgroundColor: item._view.backgroundColor,
            //     value: this.values[item._index]
            // })
        }
    },
    mounted() {
        // Overwriting base render method with actual data.
        this.renderChart(this.chartData, this.options)
    }
}
</script>