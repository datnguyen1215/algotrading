<script>
  import { onMount } from 'svelte';
  import Highcharts from 'highcharts';

  let dom = {
    /** @type {HTMLElement}*/
    chart: null
  };

  onMount(() => {
    // const chart = Highcharts.chart(dom.chart, {
    //   title: {
    //     text: 'My chart'
    //   }
    // });
    // return () => {
    //   chart.destroy();
    // };
  });
</script>

<div bind:this={dom.chart} class="w-full h-full flex items-center flex-col">
  This should display chart
</div>
