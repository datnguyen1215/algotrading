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

  const onSymbolClicked = symbol => {
    console.log(symbol);
  };

  onMount(async () => {
    try {
      symbols = await api.v1.symbols.get();
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

<div>
  {#if symbols.length}
    <h2 class="py-5 text-center font-bold pointer-events-none select-none">Symbols</h2>

    <div>
      {#each symbols as symbol}
        <button on:click={() => onSymbolClicked(symbol)} class="block">
          <span class="px-5 hover:bg-gray-200 select-none">{symbol.name}</span>
        </button>
      {/each}
    </div>
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
