{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "DownloadLineSticker.ipynb",
      "provenance": [],
      "collapsed_sections": [],
      "authorship_tag": "ABX9TyP6Zmnr5wej3s6Pz9AvpLVv",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/sagelga/line-to-telegram-sticker/blob/master/run.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "htig2uHlPzHS",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 1000
        },
        "outputId": "595d62c3-33b7-4b63-ab13-9f1ee87d7e27"
      },
      "source": [
        "# Installing the libraries\n",
        "import os\n",
        "import requests\n",
        "\n",
        "import PIL\n",
        "from PIL import Image\n",
        "from io import BytesIO\n",
        "from google.colab import files\n",
        "\n",
        "DEST_FOLDER = ''\n",
        "FILE_PREFIX = 'sticker'\n",
        "BASE_URL_PREFIX = 'https://stickershop.line-scdn.net/stickershop/v1/sticker/'\n",
        "BASE_URL_SUFFIX = \"/android/sticker.png\"\n",
        "PREFERENCE_SIZE = 512\n",
        "# https://stickershop.line-scdn.net/stickershop/v1/sticker/324744790/android/sticker.png\n",
        "\n",
        "def main():\n",
        "    # Check for configuration error\n",
        "    if (DEST_FOLDER != '') and (not os.path.exists(DEST_FOLDER)):\n",
        "        raise Exception(\"Folder doesn't exist\")\n",
        "\n",
        "    # Retrieve sticker ID\n",
        "    FIRST_ID = abs(int(input('First Sticker ID : ')))\n",
        "\n",
        "    # Retrieve sticker count\n",
        "    retry = 0\n",
        "    STICKER_COUNT = 0\n",
        "    while (STICKER_COUNT <= 0 or retry > 2):\n",
        "        STICKER_COUNT = int(input('Sticker count in the pack : '))\n",
        "        retry += 1\n",
        "\n",
        "    for i in range(STICKER_COUNT):\n",
        "        stickerRetrieve(FIRST_ID + i)\n",
        "\n",
        "\n",
        "def stickerRetrieve(id):\n",
        "    id = str(id)\n",
        "\n",
        "    url = BASE_URL_PREFIX + id + BASE_URL_SUFFIX\n",
        "    print(\"-------------------------------------\")\n",
        "    print('Downloading from : '+url)\n",
        "\n",
        "    try:\n",
        "        # Retrive binaries\n",
        "        img = requests.get(url, timeout=(10, 30))\n",
        "        img.raise_for_status()\n",
        "    except Timeout as identifier:\n",
        "        # https://2.python-requests.org//en/master/user/quickstart/#timeouts\n",
        "        print('Timeout')\n",
        "    except TooManyRedirects:\n",
        "        print('Too many redirects')\n",
        "    except HTTPError:\n",
        "        print('Unable to have HTTP connection')\n",
        "\n",
        "    # Converts the image into a Telegram friendly size\n",
        "    try:\n",
        "        img = Image.open(BytesIO(img.content))\n",
        "        print(\"Raw size :\", str(img.size[0]) + \" x \" + str(img.size[1]))\n",
        "\n",
        "        if max(img.size[0], img.size[1]) == img.size[1]:\n",
        "            ratio = (PREFERENCE_SIZE / float(img.size[1]))\n",
        "            wsize = int((float(img.size[0]) * float(ratio)))\n",
        "            img = img.resize((wsize, PREFERENCE_SIZE), PIL.Image.ANTIALIAS)\n",
        "        else:\n",
        "            ratio = (PREFERENCE_SIZE / float(img.size[0]))\n",
        "            wsize = int((float(img.size[1]) * float(ratio)))\n",
        "            img = img.resize((PREFERENCE_SIZE, wsize), PIL.Image.ANTIALIAS)\n",
        "\n",
        "        print(\"New size :\", str(img.size[0]), \"x\", str(img.size[1]))\n",
        "\n",
        "        # Save the file, where it should be\n",
        "        img_dest =  id + '.png'\n",
        "        img.save(img_dest)\n",
        "        \n",
        "        # print(type(img_dest))\n",
        "        files.download(str(img_dest)) \n",
        "        # print(\"Sticker destination : \" + str(img_dest))\n",
        "\n",
        "    except IOError as identifier:\n",
        "        pass\n",
        "    except KeyError as identifier:\n",
        "        pass\n",
        "\n",
        "\n",
        "main()"
      ],
      "execution_count": 1,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "First Sticker ID : 61897334\n",
            "Sticker count in the pack : 40\n",
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897334/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_f1fa01f6-3741-4c6c-bbeb-6077144c68df\", \"61897334.png\", 15176)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897335/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_99cfbdee-51a5-4c98-b85d-06b12c7dae9a\", \"61897335.png\", 15043)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897336/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_a8a6bbd6-23bf-4f27-b6fe-67dd1afdd17e\", \"61897336.png\", 17161)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897337/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_b30aa6e6-e05e-464f-a411-3f69b00ee9bd\", \"61897337.png\", 18004)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897338/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_04770f91-15e6-4484-b005-edb8e3ad7db4\", \"61897338.png\", 19713)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897339/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_9bff0adb-5976-4273-ba6b-a001a9a6e90b\", \"61897339.png\", 16876)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897340/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_e18d15f8-e655-4275-8c61-ca8d860901e1\", \"61897340.png\", 18260)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897341/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_47dd2912-7888-4012-8414-bef309ca0eb2\", \"61897341.png\", 17554)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897342/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_a7c6dd4e-36dd-4f7e-9a9e-4798737562ad\", \"61897342.png\", 20056)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897343/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_2aa74fd0-b14c-484c-be11-ec8bddad0ae1\", \"61897343.png\", 20271)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897344/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_3dfa39e5-cb21-41c4-bd04-ff58a7707061\", \"61897344.png\", 14688)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897345/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_85284bdc-416a-4281-8c17-653c1e4bbf4b\", \"61897345.png\", 16384)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897346/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_f21b1a4f-2abb-41ff-9d95-4acc7be20c97\", \"61897346.png\", 17383)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897347/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_0b2b8552-8ee5-4cc0-92a5-c154f282c82e\", \"61897347.png\", 16042)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897348/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_b91074fb-1f65-4798-b3ea-5290e577f614\", \"61897348.png\", 16720)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897349/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_7b6c3f92-1ed9-487f-88bd-3b8eea01ae63\", \"61897349.png\", 22001)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897350/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_a3792313-5856-4635-b6c8-c32de57132a0\", \"61897350.png\", 17576)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897351/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_23d4cbc3-7f3c-4c2e-b4d9-24cc18b52f1a\", \"61897351.png\", 21707)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897352/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_fe539ca1-b7cf-4636-839d-95b75bc1d288\", \"61897352.png\", 14718)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897353/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_08b77916-0d38-4693-9dc9-6d21eba91aeb\", \"61897353.png\", 20957)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897354/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_f87d8210-b7f2-4c3f-b1c6-4e414ad749a5\", \"61897354.png\", 14886)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897355/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_c1ca1554-db7c-4d97-852e-4166ff3722cb\", \"61897355.png\", 15865)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897356/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_f66ee3b9-4073-4a15-8df4-50a8010765b1\", \"61897356.png\", 15775)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897357/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_c4529ef2-24c6-4b3c-bbad-6e45a795e517\", \"61897357.png\", 16393)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897358/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_e5fd3099-745d-4a97-b344-136ac4d046dc\", \"61897358.png\", 17209)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897359/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_fed73272-9f03-4ace-8d7b-e4032db59e63\", \"61897359.png\", 17065)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897360/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_9e10e25b-5590-4a8a-8a2f-f5beb37f86ac\", \"61897360.png\", 22672)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897361/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_4eac5d4f-d71a-48f1-ae83-b644f5621a61\", \"61897361.png\", 21825)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897362/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_3b742d58-66b8-4d09-b0b6-fc778d970e19\", \"61897362.png\", 22744)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897363/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_30027706-5c3a-4f1b-937e-81180f9ea811\", \"61897363.png\", 21240)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897364/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_d56a4ff2-ef4b-4e30-9c53-b2f68f9ab8ae\", \"61897364.png\", 14903)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897365/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_bfa883af-5706-44df-84fe-45137d13fa01\", \"61897365.png\", 19456)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897366/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_e88b1765-6e2a-4cc9-a78d-4c40dfaaa03b\", \"61897366.png\", 16138)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897367/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_03ed609c-5c95-4188-8ce1-541693d1dbb1\", \"61897367.png\", 14606)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897368/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_f0270c81-0878-4123-a2fa-7db23b567531\", \"61897368.png\", 15435)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897369/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_6623fe9e-4ab8-469e-b63d-92dcb5dfeb2b\", \"61897369.png\", 19071)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897370/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_2598772b-0883-40f8-a707-50c35e7f9c6e\", \"61897370.png\", 14347)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897371/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_fe83cf98-d936-47a6-aa10-a0501744c8bc\", \"61897371.png\", 14587)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897372/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_ffec90b8-00fa-466a-a533-24884d6c946f\", \"61897372.png\", 22330)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "stream",
          "text": [
            "-------------------------------------\n",
            "Downloading from : https://stickershop.line-scdn.net/stickershop/v1/sticker/61897373/android/sticker.png\n",
            "Raw size : 259 x 224\n",
            "New size : 512 x 442\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        },
        {
          "output_type": "display_data",
          "data": {
            "application/javascript": [
              "download(\"download_f4f0bc19-e02c-474d-a9b9-ae6618cd1581\", \"61897373.png\", 15211)"
            ],
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ]
          },
          "metadata": {
            "tags": []
          }
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "VWKPtirFSxsh",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        ""
      ],
      "execution_count": null,
      "outputs": []
    }
  ]
}