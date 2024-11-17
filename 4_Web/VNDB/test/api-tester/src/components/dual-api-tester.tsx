'use client'

import { useState, useEffect, useRef } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { useTheme } from "next-themes"
import { Moon, Sun, Bookmark, List, Trash2, ImageIcon, Upload, X } from 'lucide-react'

interface Param {
  key: string
  value: string
}

interface BookmarkData {
  id: number
  name: string
  host: string
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

function Bookmarks({ host, onLoadBookmark }: { host: string, onLoadBookmark: (bookmark: BookmarkData) => void }) {
  const [bookmarks, setBookmarks] = useState<BookmarkData[]>([])
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchBookmarks()
  }, [host])

  const fetchBookmarks = async () => {
    try {
      const res = await fetch(`${host}/api/bookmarks`)
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`)
      }
      const data = await res.json()
      setBookmarks(data)
      setError(null)
    } catch (error) {
      console.error('Error fetching bookmarks:', error)
      setError(`Error fetching bookmarks: ${error instanceof Error ? error.message : String(error)}`)
    }
  }

  const deleteBookmark = async (id: number, e: React.MouseEvent) => {
    e.stopPropagation()
    try {
      const res = await fetch(`${host}/api/bookmarks/${id}`, {
        method: 'DELETE',
      })
      if (res.ok) {
        fetchBookmarks()
      } else {
        throw new Error('Failed to delete bookmark')
      }
    } catch (error) {
      console.error('Error deleting bookmark:', error)
      setError(`Error deleting bookmark: ${error instanceof Error ? error.message : String(error)}`)
    }
  }

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Bookmarks</h2>
      {bookmarks.map((bookmark) => (
        <Card 
          key={bookmark.id} 
          className="p-4 hover:bg-accent transition-colors cursor-pointer"
          onClick={() => onLoadBookmark(bookmark)}
        >
          <CardContent className="p-0">
            <div className="flex justify-between items-center">
              <div className="flex-grow">
                <div className="font-bold">{bookmark.name || `${bookmark.method} ${bookmark.route}`}</div>
                <div className="text-sm text-muted-foreground">
                  {bookmark.name && `${bookmark.method} ${bookmark.route}`}
                </div>
                <div className="text-sm text-muted-foreground">
                  {bookmark.host}
                </div>
                <div className="text-sm text-muted-foreground">
                  {new Date(bookmark.created_at).toLocaleString()}
                </div>
              </div>
              <Button 
                variant="ghost" 
                size="icon" 
                onClick={(e) => deleteBookmark(bookmark.id, e)}
                className="ml-2"
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          </CardContent>
        </Card>
      ))}
      {bookmarks.length === 0 && !error && (
        <div className="text-muted-foreground text-sm">No bookmarks found.</div>
      )}
      {error && (
        <div className="text-destructive text-sm mt-2">
          {error}
        </div>
      )}
    </div>
  )
}

function RequestForm({ onSubmit }: { onSubmit: (formData: any) => void }) {
  const [apiHost, setApiHost] = useState('')
  const [endpoint, setEndpoint] = useState('')
  const [method, setMethod] = useState('GET')
  const [body, setBody] = useState('')
  const [params, setParams] = useState<Param[]>([{ key: '', value: '' }])
  const [files, setFiles] = useState<File[]>([])
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [suggestions, setSuggestions] = useState<string[]>([])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit({ apiHost, endpoint, method, body, params, files })
  }

  const addParam = () => {
    setParams([...params, { key: '', value: '' }])
  }

  const updateParam = (index: number, field: keyof Param, value: string) => {
    const newParams = [...params]
    newParams[index][field] = value
    setParams(newParams)
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFiles(Array.from(e.target.files))
    }
  }

  const triggerFileInput = () => {
    fileInputRef.current?.click()
  }

  const clearFiles = () => {
    setFiles([])
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const formatFileInfo = (file: File) => {
    const lastModified = new Date(file.lastModified).toLocaleString()
    return `${file.name} (Last modified: ${lastModified})`
  }

  const handleApiHostChange = (value: string) => {
    setApiHost(value)
    if (value.startsWith('http://') || value.startsWith('https://')) {
      setSuggestions([])
    } else {
      setSuggestions([
        `http://${value}`,
        `https://${value}`,
        `http://www.${value}`,
        `https://www.${value}`,
      ])
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="flex flex-col space-y-2">
        <Input
          type="text"
          value={apiHost}
          onChange={(e) => handleApiHostChange(e.target.value)}
          placeholder="Enter API host (e.g., localhost:8000)"
          className="flex-grow"
          required
        />
        {suggestions.length > 0 && (
          <ul className="bg-background border border-input rounded-md mt-1">
            {suggestions.map((suggestion, index) => (
              <li
                key={index}
                className="px-3 py-2 hover:bg-accent cursor-pointer"
                onClick={() => {
                  setApiHost(suggestion)
                  setSuggestions([])
                }}
              >
                {suggestion}
              </li>
            ))}
          </ul>
        )}
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
        <Select value={method} onValueChange={(value) => setMethod(value)}>
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
          <TabsTrigger value="files">Files</TabsTrigger>
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
        <TabsContent value="files">
          <div className="space-y-2">
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileChange}
              multiple
              className="hidden"
            />
            <div className="flex space-x-2">
              <Button type="button" onClick={triggerFileInput} variant="outline" className="flex-grow">
                <Upload className="mr-2 h-4 w-4" /> Select Files
              </Button>
              <Button type="button" onClick={clearFiles} variant="outline" className="flex-shrink-0">
                <X className="h-4 w-4" />
              </Button>
            </div>
            {files.length > 0 && (
              <div className="mt-2">
                <h3 className="font-semibold">Selected Files:</h3>
                <ul className="list-disc pl-5">
                  {files.map((file, index) => (
                    <li key={index}>{formatFileInfo(file)}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </TabsContent>
      </Tabs>
      <Button type="submit" className="w-full">
        Send Request
      </Button>
    </form>
  )
}

export default function EnhancedDualAPITester() {
  const [bookmarksHost] = useState('http://localhost:5050')
  const [response1, setResponse1] = useState('')
  const [response2, setResponse2] = useState('')
  const [loading1, setLoading1] = useState(false)
  const [loading2, setLoading2] = useState(false)
  const [imageUrl1, setImageUrl1] = useState('')
  const [imageUrl2, setImageUrl2] = useState('')
  const [showImage1, setShowImage1] = useState(false)
  const [showImage2, setShowImage2] = useState(false)
  const { theme, setTheme } = useTheme()
  const [mounted, setMounted] = useState(false)
  const [showBookmarks, setShowBookmarks] = useState(false)
  const [showSaveDialog, setShowSaveDialog] = useState(false)
  const [responseFormat, setResponseFormat] = useState('auto')

  useEffect(() => {
    setMounted(true)
  }, [])

  const handleSubmit = async (formData: any, setResponse: (response: string) => void, setLoading: (loading: boolean) => void, setImageUrl: (url: string) => void, setShowImage: (show: boolean) => void) => {
    setLoading(true)
    setResponse('')
    setImageUrl('')
    setShowImage(false)

    try {
      const url = new URL(formData.endpoint, formData.apiHost);
      formData.params.forEach((param: Param) => {
        if (param.key.trim() && param.value.trim()) {
          url.searchParams.append(param.key.trim(), param.value.trim());
        }
      });

      let options: RequestInit = {
        method: formData.method,
        headers: {},
      }

      if (['POST', 'PUT', 'PATCH'].includes(formData.method)) {
        if (formData.files.length > 0) {
          const formDataObj = new FormData()
          formData.files.forEach((file: File) => {
            formDataObj.append('files[]', file)
            formDataObj.append(`last_modified_${file.name}`, file.lastModified.toString())
          })
          if (formData.body) {
            formDataObj.append('json', formData.body)
          }
          options.body = formDataObj
        } else if (formData.body) {
          options.headers['Content-Type'] = 'application/json'
          options.body = formData.body
        }
      }

      const res = await fetch(url.toString(), options)

      const contentType = res.headers.get('content-type')
      
      if (contentType && contentType.includes('image')) {
        const blob = await res.blob()
        const imageUrl = URL.createObjectURL(blob)
        setImageUrl(imageUrl)
        setShowImage(true)
        setResponse('Image received. Click "Show Image" to view.')
      } else {
        const responseText = await res.text()
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
      }
    } catch (error) {
      setResponse(`Error: ${error instanceof Error ? error.message : String(error)}`)
    } finally {
      setLoading(false)
    }
  }

  const saveBookmark = async (name: string) => {
    try {
      const res = await fetch(`${bookmarksHost}/api/bookmarks`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name,
          host: 'example.com',
          route: '/api/example',
          method: 'GET',
          params: '{}',
          body: '',
        }),
      });
      if (res.ok) {
        setShowBookmarks(true);
      } else {
        throw new Error('Failed to save bookmark');
      }
    } catch (error) {
      console.error('Error saving bookmark:', error);
    }
  }

  const loadBookmark = (bookmark: BookmarkData) => {
    // Implementation for loading a bookmark
    console.log('Loading bookmark:', bookmark);
    setShowBookmarks(false);
  }

  const clearResults = (index: number) => {
    if (index === 1) {
      setResponse1('')
      setImageUrl1('')
      setShowImage1(false)
    } else {
      setResponse2('')
      setImageUrl2('')
      setShowImage2(false)
    }
  }

  const toggleImageDisplay = (index: number) => {
    if (index === 1) {
      setShowImage1(!showImage1)
    } else {
      setShowImage2(!showImage2)
    }
  }

  if (!mounted) {
    return null
  }

  return (
    <Card className="w-full max-w-7xl mx-auto">
      <CardHeader>
        <div className="flex justify-between items-center">
          <CardTitle className="text-2xl font-bold">Enhanced Dual API Tester</CardTitle>
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
          <div className="flex flex-col lg:flex-row gap-8">
            <div className="flex-1">
              <h2 className="text-xl font-semibold mb-4">Request Form 1</h2>
              <RequestForm onSubmit={(formData) => handleSubmit(formData, setResponse1, setLoading1, setImageUrl1, setShowImage1)} />
              {(response1 || imageUrl1) && (
                <div className="mt-4">
                  <div className="flex justify-between items-center mb-2">
                    <h3 className="text-lg font-semibold">Response 1:</h3>
                    <div className="flex space-x-2">
                      {imageUrl1 && (
                        <Button variant="outline" size="sm" onClick={() => toggleImageDisplay(1)}>
                          <ImageIcon className="h-4 w-4 mr-2" />
                          {showImage1 ? 'Hide Image' : 'Show Image'}
                        </Button>
                      )}
                      <Button variant="ghost" size="sm" onClick={() => clearResults(1)}>
                        <Trash2 className="h-4 w-4 mr-2" />
                        Clear Results
                      </Button>
                    </div>
                  </div>
                  {showImage1 && imageUrl1 ? (
                    <div className="mt-4">
                      <img src={imageUrl1} alt="API Response 1" className="max-w-full h-auto" />
                    </div>
                  ) : (
                    <div className="bg-secondary p-4 rounded-md overflow-x-auto max-h-[400px]">
                      <pre className="whitespace-pre-wrap break-words">
                        <code>{response1}</code>
                      </pre>
                    </div>
                  )}
                </div>
              )}
            </div>
            <div className="w-px bg-border self-stretch hidden lg:block" />
            <div className="flex-1">
              <h2 className="text-xl font-semibold mb-4">Request Form 2</h2>
              <RequestForm onSubmit={(formData) => handleSubmit(formData, setResponse2, setLoading2, setImageUrl2, setShowImage2)} />
              {(response2 || imageUrl2) && (
                <div className="mt-4">
                  <div className="flex justify-between items-center mb-2">
                    <h3 className="text-lg font-semibold">Response 2:</h3>
                    <div className="flex space-x-2">
                      {imageUrl2 && (
                        <Button variant="outline" size="sm" onClick={() => toggleImageDisplay(2)}>
                          <ImageIcon className="h-4 w-4 mr-2" />
                          {showImage2 ? 'Hide Image' : 'Show Image'}
                        </Button>
                      )}
                      <Button variant="ghost" size="sm" onClick={() => clearResults(2)}>
                        <Trash2 className="h-4 w-4 mr-2" />
                        Clear Results
                      </Button>
                    </div>
                  </div>
                  {showImage2 && imageUrl2 ? (
                    <div className="mt-4">
                      <img src={imageUrl2} alt="API Response 2" className="max-w-full h-auto" />
                    </div>
                  ) : (
                    <div className="bg-secondary p-4 rounded-md overflow-x-auto max-h-[400px]">
                      <pre className="whitespace-pre-wrap break-words">
                        <code>{response2}</code>
                      </pre>
                    </div>
                  )}
                </div>
              )}
            </div>
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