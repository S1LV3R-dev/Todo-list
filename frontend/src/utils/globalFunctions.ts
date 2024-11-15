export async function request(
  url: string,
  method: 'GET' | 'POST' | 'PUT' | 'DELETE',
  data: Record<string, unknown>,
  auth_token: string = '',
): Promise<{ body: unknown[]; status: number }> {
  let response
  const api_url = 'http://localhost:5000'
  const cleanedData = JSON.parse(JSON.stringify(data)) // Clean input data
  try {
    // Handle GET requests
    if (method === 'GET') {
      const requestString = new URLSearchParams(cleanedData).toString()
      response = await fetch(`${api_url}/api${url}?${requestString}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${auth_token}`,
        },
      })
    }
    // Handle POST, PUT, DELETE, etc.
    else {
      response = await fetch(`${api_url}/api${url}`, {
        method: method,
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${auth_token}`,
        },
        body: JSON.stringify(cleanedData),
      })
    }
    return { body: await response.json(), status: response.status } // Return parsed JSON or empty array
  } catch (error) {
    console.error('Error during request:', error)
    return { body: [], status: 0 } // Return an empty array for network or parsing errors
  }
}
