<script>
  import api from '$lib/api';
  import Spinner from '$lib/components/Common/Spinner.svelte';
  import { onMount } from 'svelte';

  let spinner = {
    show: true,
    message: 'Loading symbols...'
  };

  let error = {
    show: false,
    message: ''
  };

  let symbols = [];

  onMount(() => {
    (async () => {
      try {
        const result = await api.v1.symbols.get();
        symbols = result.map(x => x.name);
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
    })();
  });
</script>

<div>
  {#if symbols.length}
    <ul>
      <h2>Symbols</h2>

      {#each symbols as symbol}
        <li>{symbol}</li>
      {/each}
    </ul>
  {/if}

  {#if spinner.show}
    <div class="flex flex-col items-center">
      <Spinner class="w-10 h-10" color="#6F6FFF" />
      <p>{spinner.message}</p>
    </div>
  {/if}

  {#if error.show}
    <div class="flex flex-col items-center">
      <p class="error">{error.message}</p>
    </div>
  {/if}
</div>
