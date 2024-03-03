<script>
  import HighChart from './HighChart.svelte';
  import Spinner from '../Common/Spinner.svelte';
  import { onMount } from 'svelte';
  import api from '$lib/api';

  export let symbol;

  let spinner = {
    show: true,
    message: 'Loading chart...'
  };

  let error = {
    show: false,
    message: ''
  };

  onMount(async () => {
    try {
      const candles = await api.v1.candles.get({
        symbol: symbol.name,
        interval: 'm1',
        from: '2021-01-01'
      });

      console.log(candles);
    } catch (err) {
      error = {
        show: true,
        message: err.message
      };
    } finally {
      spinner = {
        show: false,
        message: ''
      };
    }
  });
</script>

<div class="w-full h-full">
  {#if !spinner.show && !error.show}
    <HighChart />
  {/if}

  {#if spinner.show}
    <div class="flex flex-col items-center">
      <Spinner class="w-10 h-10" color="#6F6FFF" />
      <p>{spinner.message}</p>
    </div>
  {/if}

  {#if error.show}
    <div class="flex flex-col items-center">
      <p>{error.message}</p>
    </div>
  {/if}
</div>
