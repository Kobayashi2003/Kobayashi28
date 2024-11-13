'use client'

import { useState, useEffect } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { useTheme } from "next-themes"
import { Moon, Sun, Bookmark, List, Trash2 } from 'lucide-react'
import Bookmarks from './bookmarks'

interface Param {
  key: string
  value: string
}

interface BookmarkData {
  id: number
  name: string
  host: string // Ensure host is included in the BookmarkData interface
  route: string
  method: string
  params: string
  body: string
  created_at: string
}

interface SaveBookmarkDialogProps {
  isOpen: boolean
  onClose: () => void
  onSave: (name: string) => void
}

function SaveBookmarkDialog({ isOpen, onClose, onSave }: SaveBookmarkDialogProps) {
  const [name, setName] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSave(name)
    setName('')
    onClose()
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Save Bookmark</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="name">Bookmark Name</Label>
              <Input
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Enter a name for this bookmark"
                autoFocus
              />
            </div>
            <div className="flex justify-end space-x-2">
              <Button type="button" variant="outline" onClick={onClose}>
                Cancel
              </Button>
              <Button type="submit">
                Save
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

export default function APITester() {
  const [bookmarksHost] = useState('http://localhost:5050')
  const [apiHost, setApiHost] = useState('')
  const [endpoint, setEndpoint] = useState('')
  const [method, setMethod] = useState('GET')
  const [body, setBody] = useState('')
  const [response, setResponse] = useState('')
  const [loading, setLoading] = useState(false)
  const [taskId, setTaskId] = useState('')
  const [autoFetch, setAutoFetch] = useState(true)
  const [params, setParams] = useState<Param[]>([{ key: '', value: '' }])
  const { theme, setTheme } = useTheme()
  const [mounted, setMounted] = useState(false)
  const [showBookmarks, setShowBookmarks] = useState(false)
  const [showSaveDialog, setShowSaveDialog] = useState(false)
  const [responseFormat, setResponseFormat] = useState('auto')

  useEffect(() => {
    setMounted(true)
  }, [])

  useEffect(() => {
    let intervalId: NodeJS.Timeout | null = null;
    if (taskId && autoFetch) {
      intervalId = setInterval(fetchTaskStatus, 2000);
    }
    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [taskId, autoFetch]);

  // Clear response when form inputs change
  useEffect(() => {
    setResponse('')
  }, [apiHost, endpoint, method, body, params])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setResponse('')
    setTaskId('')

    try {
      const options: RequestInit = {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
      }

      if (['POST', 'PUT'].includes(method) && body) {
        options.body = body
      }

      const url = new URL(endpoint, apiHost);
      // Only add non-empty parameters
      params.forEach(param => {
        if (param.key.trim() && param.value.trim()) {
          url.searchParams.append(param.key.trim(), param.value.trim());
        }
      });

      const res = await fetch(url.toString(), options)
      const responseText = await res.text()

      // Parse response based on selected format
      let parsedResponse
      if (responseFormat === 'auto') {
        try {
          parsedResponse = JSON.parse(responseText)
        } catch {
          parsedResponse = responseText
        }
      } else if (responseFormat === 'json') {
        parsedResponse = JSON.parse(responseText)
      } else {
        parsedResponse = responseText
      }

      setResponse(typeof parsedResponse === 'string' ? parsedResponse : JSON.stringify(parsedResponse, null, 2))

      if (parsedResponse.task_id) {
        setTaskId(parsedResponse.task_id)
      }
    } catch (error) {
      setResponse(`Error: ${error instanceof Error ? error.message : String(error)}`)
    } finally {
      setLoading(false)
    }
  }

  const fetchTaskStatus = async () => {
    if (!taskId) return;

    try {
      const url = new URL(`/api/status/${taskId}`, apiHost);
      const res = await fetch(url.toString())
      const data = await res.json()
      setResponse(JSON.stringify(data, null, 2))

      if (data.state === 'SUCCESS' || data.state === 'FAILURE') {
        setTaskId('')
      }
    } catch (error) {
      setResponse(`Error fetching task status: ${error instanceof Error ? error.message : String(error)}`)
      setTaskId('')
    }
  }

  const addParam = () => {
    setParams([...params, { key: '', value: '' }])
  }

  const updateParam = (index: number, field: keyof Param, value: string) => {
    const newParams = [...params]
    newParams[index][field] = value
    setParams(newParams)
  }

  const saveBookmark = async (name: string) => {
    try {
      // Only filter non-empty parameters
      const validParams = params.filter(param => param.key.trim() && param.value.trim());

      const res = await fetch(`${bookmarksHost}/api/bookmarks`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name,
          host: apiHost, // Save the host along with the URI
          route: endpoint,
          method,
          params: JSON.stringify(validParams),
          body,
        }),
      });
      if (res.ok) {
        setShowBookmarks(true);
      } else {
        throw new Error('Failed to save bookmark');
      }
    } catch (error) {
      console.error('Error saving bookmark:', error);
      setResponse(`Error saving bookmark: ${error instanceof Error ? error.message : String(error)}`);
    }
  }

  const loadBookmark = (bookmark: BookmarkData) => {
    setApiHost(bookmark.host); // Set the API host from the bookmark
    setEndpoint(bookmark.route);
    setMethod(bookmark.method);
    try {
      const parsedParams = JSON.parse(bookmark.params);
      // Ensure parsedParams is an array
      const paramArray = Array.isArray(parsedParams) ? parsedParams : [];
      setParams([...paramArray, { key: '', value: '' }]);
    } catch (error) {
      console.error('Error parsing parameters:', error);
      setParams([{ key: '', value: '' }]);
    }
    setBody(bookmark.body);
    setShowBookmarks(false);
  }

  const handleApiHostChange = (value: string) => {
    // Auto-complete localhost URLs
    if (value.startsWith('localhost')) {
      value = `http://${value}`;
    }
    setApiHost(value);
  };

  const clearResults = () => {
    setResponse('');
    setTaskId('');
  }

  if (!mounted) {
    return null
  }

  return (
    <Card className="w-full max-w-4xl mx-auto">
      <CardHeader>
        <div className="flex justify-between items-center">
          <CardTitle className="text-2xl font-bold">Enhanced API Tester</CardTitle>
          <div className="flex space-x-2">
            <Button variant="ghost" size="icon" onClick={() => setShowBookmarks(!showBookmarks)}>
              <List className="h-6 w-6" />
            </Button>
            <Button variant="ghost" size="icon" onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}>
              {theme === 'dark' ? <Sun className="h-6 w-6" /> : <Moon className="h-6 w-6" />}
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        {showBookmarks ? (
          <Bookmarks host={bookmarksHost} onLoadBookmark={loadBookmark} />
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="flex space-x-2">
              <Input
                type="text"
                value={apiHost}
                onChange={(e) => handleApiHostChange(e.target.value)}
                placeholder="Enter API host (e.g., localhost:8000)"
                className="flex-grow"
                required
              />
            </div>
            <div className="flex space-x-2">
              <Input
                type="text"
                value={endpoint}
                onChange={(e) => setEndpoint(e.target.value)}
                placeholder="Enter API endpoint (e.g., /api/data)"
                className="flex-grow"
                required
              />
              <Select value={method} onValueChange={setMethod}>
                <SelectTrigger className="w-[180px]">
                  <SelectValue placeholder="Select method" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="GET">GET</SelectItem>
                  <SelectItem value="POST">POST</SelectItem>
                  <SelectItem value="PUT">PUT</SelectItem>
                  <SelectItem value="DELETE">DELETE</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <Tabs defaultValue="params" className="w-full">
              <TabsList>
                <TabsTrigger value="params">Query Parameters</TabsTrigger>
                <TabsTrigger value="body">Request Body</TabsTrigger>
              </TabsList>
              <TabsContent value="params">
                <div className="space-y-2">
                  {params.map((param, index) => (
                    <div key={index} className="flex space-x-2">
                      <Input
                        type="text"
                        value={param.key}
                        onChange={(e) => updateParam(index, 'key', e.target.value)}
                        placeholder="Key"
                        className="flex-grow"
                      />
                      <Input
                        type="text"
                        value={param.value}
                        onChange={(e) => updateParam(index, 'value', e.target.value)}
                        placeholder="Value"
                        className="flex-grow"
                      />
                    </div>
                  ))}
                  <Button type="button" onClick={addParam} variant="outline" className="w-full">
                    Add Parameter
                  </Button>
                </div>
              </TabsContent>
              <TabsContent value="body">
                <Textarea
                  value={body}
                  onChange={(e) => setBody(e.target.value)}
                  placeholder="Enter request body (JSON)"
                  className="min-h-[200px]"
                />
              </TabsContent>
            </Tabs>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <Switch
                  id="auto-fetch"
                  checked={autoFetch}
                  onCheckedChange={setAutoFetch}
                />
                <Label htmlFor="auto-fetch">Auto-fetch task status</Label>
              </div>
              <Select value={responseFormat} onValueChange={setResponseFormat}>
                <SelectTrigger className="w-[180px]">
                  <SelectValue placeholder="Response format" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="auto">Auto</SelectItem>
                  <SelectItem value="json">JSON</SelectItem>
                  <SelectItem value="plain">Plain text</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="flex space-x-2">
              <Button type="submit" disabled={loading} className="flex-grow">
                {loading ? 'Sending...' : 'Send Request'}
              </Button>
              <Button type="button" onClick={() => setShowSaveDialog(true)} variant="outline">
                <Bookmark className="h-4 w-4 mr-2" />
                Bookmark
              </Button>
            </div>
          </form>
        )}
        {response && (
          <div className="mt-4">
            <div className="flex justify-between items-center mb-2">
              <h2 className="text-xl font-semibold">Response:</h2>
              <Button variant="ghost" size="sm" onClick={clearResults}>
                <Trash2 className="h-4 w-4 mr-2" />
                Clear Results
              </Button>
            </div>
            <pre className="bg-secondary p-4 rounded-md overflow-x-auto">
              <code>{response}</code>
            </pre>
          </div>
        )}
      </CardContent>
      <SaveBookmarkDialog
        isOpen={showSaveDialog}
        onClose={() => setShowSaveDialog(false)}
        onSave={saveBookmark}
      />
    </Card>
  )
}