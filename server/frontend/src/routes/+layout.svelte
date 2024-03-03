<script>
  import '../app.css';
  import Sidebar from '$lib/components/Common/Sidebar/Container.svelte';
  import Spinner from '$lib/components/Common/Spinner.svelte';
  import { onMount } from 'svelte';
  import selectedSymbol from '$lib/stores/selectedSymbol';
  import symbols from '$lib/stores/symbols';
  import api from '$lib/api';

  let spinner = {
    show: true,
    message: 'Loading data...'
  };

  let error = {
    show: false,
    message: ''
  };

  /**
   * Get the selected symbol from local storage
   * @returns {Symbol|null}
   */
  const getSelectedSymbol = () => {
    spinner = {
      show: true,
      message: 'Loading selected symbol...'
    };

    const s = localStorage.getItem('selectedSymbol');

    if (!s) return null;

    return JSON.parse(localStorage.getItem('selectedSymbol'));
  };

  /**
   * Get the symbols from the API
   * @returns {Promise<Symbol[]>}
   */
  const getSymbols = async () => {
    spinner = {
      show: true,
      message: 'Loading symbols...'
    };
    return await api.v1.symbols.get();
  };

  onMount(async () => {
    try {
      $selectedSymbol = getSelectedSymbol();
      $symbols = await getSymbols();
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

<div class="flex h-full">
  {#if spinner.show}
    <div class="flex flex-col items-center m-auto">
      <Spinner class="w-10 h-10" />
      <p>{spinner.message}</p>
    </div>
  {/if}

  {#if !spinner.show}
    <Sidebar />
    <slot />
  {/if}

  {#if error.show}
    <div class="flex flex-col items-center">
      <p class="error">{error.message}</p>
    </div>
  {/if}
</div>
