import VueCookie from "vue-cookie";

export async function request(
  url: string,
  method: 'GET' | 'POST' | 'PUT' | 'DELETE',
  data: Record<string, unknown> = {},
): Promise<{ body: unknown[]; status: number }> {
  let response
  // const api_url = 'https://anxiously-allowed-martin.cloudpub.ru:443'
  const api_url = 'http://localhost:5000'
  const cleanedData = JSON.parse(JSON.stringify(data)) // Clean input data
  try {
    // Handle GET requests
    if (method === 'GET') {
      const requestString = new URLSearchParams(cleanedData).toString()
      response = await fetch(`${api_url}/api${url}?${requestString}`, {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
      })
    }
    // Handle POST, PUT, DELETE, etc.
    else {
      response = await fetch(`${api_url}/api${url}`, {
        method: method,
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(cleanedData),
      })
    }
    const responseData = await response.json();
    if ('token_new' in responseData){
      VueCookie.set('token', responseData.token_new)
    };
    return { body: responseData, status: response.status } // Return parsed JSON or empty array
  } catch (error) {
    console.error('Error during request:', error)
    return { body: [], status: 0 } // Return an empty array for network or parsing errors
  }
}
