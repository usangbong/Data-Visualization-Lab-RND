<script>
import { Bar , mixins } from 'vue-chartjs'

export default {
    extends: Bar,
    mixins: [mixins.reactiveProp],
    props: ['chartData'],
    data: () => ({
        type: 'Bar',
        options: {
            responsive: true,
            maintainAspectRatio: true,
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
            }
        }
    }),
    mounted() {
        // Overwriting base render method with actual data.
        this.renderChart(this.chartData, this.options)
    }
}
</script>