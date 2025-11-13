{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/pranjalup/emloy_app/blob/main/app1.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# 2A - basic network check\n",
        "!ping -c 2 google.com\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "607Y_50ojEJL",
        "outputId": "755c5311-ced9-476c-c0c9-cb7d401f5ed7"
      },
      "execution_count": 3,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "/bin/bash: line 1: ping: command not found\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# 2B - DNS SRV lookup using dnspython\n",
        "!pip install dnspython\n",
        "python_code = \"\"\"\n",
        "import dns.resolver, sys\n",
        "host = \"_mongodb._tcp.app1.utxd9yw.mongodb.net\"  # replace <cluster-id> with the one from Atlas\n",
        "try:\n",
        "    answers = dns.resolver.resolve(host, 'SRV')\n",
        "    for r in answers:\n",
        "        print(r.to_text())\n",
        "except Exception as e:\n",
        "    print(\"SRV lookup failed:\", e)\n",
        "\"\"\"\n",
        "print(python_code)\n",
        "# run it with the correct host manually in a code cell (or create below)\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "PD82FRdTjEwX",
        "outputId": "54fe5ac7-1413-4c43-8a3e-eb28651fcb54"
      },
      "execution_count": 4,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Requirement already satisfied: dnspython in /usr/local/lib/python3.12/dist-packages (2.4.2)\n",
            "\n",
            "import dns.resolver, sys\n",
            "host = \"_mongodb._tcp.app1.utxd9yw.mongodb.net\"  # replace <cluster-id> with the one from Atlas\n",
            "try:\n",
            "    answers = dns.resolver.resolve(host, 'SRV')\n",
            "    for r in answers:\n",
            "        print(r.to_text())\n",
            "except Exception as e:\n",
            "    print(\"SRV lookup failed:\", e)\n",
            "\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "from pymongo import MongoClient\n",
        "\n",
        "# ✅ use your verified URI\n",
        "uri = \"mongodb+srv://pranjalu05_db_user:divyuji2709@app1.utxd9yw.mongodb.net/?retryWrites=true&w=majority\"\n",
        "\n",
        "client = MongoClient(uri)\n",
        "db = client[\"my_database_name\"]     # create or access a database\n",
        "collection = db[\"my_collection\"]    # create or access a collection\n",
        "\n",
        "# Insert data\n",
        "collection.insert_one({\"name\": \"kshithiz\", \"role\": \"doctor\"})\n",
        "\n",
        "# Read data\n",
        "for doc in collection.find():\n",
        "    print(doc)\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "NxOMKkb-kFGS",
        "outputId": "739d4e6a-89ac-44c4-9262-ff122574042b"
      },
      "execution_count": 10,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "{'_id': ObjectId('691564c673c1a14809312279'), 'name': 'Pranjal', 'role': 'Engineer'}\n",
            "{'_id': ObjectId('6915668673c1a1480931227b'), 'name': 'Pranjal', 'role': 'Engineer'}\n",
            "{'_id': ObjectId('6915669973c1a1480931227d'), 'name': 'kshithiz', 'role': 'doctor'}\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import streamlit as st\n",
        "import pandas as pd\n",
        "from pymongo import MongoClient\n",
        "\n",
        "# --- Page Setup ---\n",
        "st.set_page_config(page_title=\"Employee Dashboard\", layout=\"wide\")\n",
        "st.title(\"💼 Employee Data Dashboard\")\n",
        "\n",
        "# --- MongoDB Connection ---\n",
        "client = MongoClient(st.secrets[\"mongodb\"][\"uri\"])\n",
        "db = client[\"employee_db\"]\n",
        "collection = db[\"employees\"]\n",
        "\n",
        "# --- Input Form ---\n",
        "st.sidebar.header(\"Add New Employee\")\n",
        "with st.sidebar.form(\"employee_form\"):\n",
        "    name = st.text_input(\"Name\")\n",
        "    role = st.text_input(\"Role\")\n",
        "    salary = st.number_input(\"Salary\", min_value=0)\n",
        "    submitted = st.form_submit_button(\"Add Employee\")\n",
        "\n",
        "if submitted and name and role:\n",
        "    collection.insert_one({\"name\": name, \"role\": role, \"salary\": salary})\n",
        "    st.success(f\"✅ Added {name} successfully!\")\n",
        "\n",
        "# --- Display Data ---\n",
        "docs = list(collection.find())\n",
        "if docs:\n",
        "    df = pd.DataFrame(docs)\n",
        "    st.dataframe(df)\n",
        "else:\n",
        "    st.info(\"No employees in the database yet.\")\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 436
        },
        "id": "5jtGGZgok6Du",
        "outputId": "95bb5ad7-47a7-411c-bec7-191e71bc712a"
      },
      "execution_count": 8,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "2025-11-13 05:02:58.467 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:02:58.469 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:02:58.469 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:02:58.471 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
          ]
        },
        {
          "output_type": "error",
          "ename": "ConfigurationError",
          "evalue": "The DNS query name does not exist: _mongodb._tcp.cluster0.mongodb.net.",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mConfigurationError\u001b[0m                        Traceback (most recent call last)",
            "\u001b[0;32m/tmp/ipython-input-2258516752.py\u001b[0m in \u001b[0;36m<cell line: 0>\u001b[0;34m()\u001b[0m\n\u001b[1;32m      8\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      9\u001b[0m \u001b[0;31m# --- MongoDB Connection ---\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 10\u001b[0;31m \u001b[0mclient\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mMongoClient\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mst\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0msecrets\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m\"mongodb\"\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m\"uri\"\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     11\u001b[0m \u001b[0mdb\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mclient\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m\"employee_db\"\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     12\u001b[0m \u001b[0mcollection\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mdb\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m\"employees\"\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.12/dist-packages/pymongo/mongo_client.py\u001b[0m in \u001b[0;36m__init__\u001b[0;34m(self, host, port, document_class, tz_aware, connect, type_registry, **kwargs)\u001b[0m\n\u001b[1;32m    772\u001b[0m                         \u001b[0mkeyword_opts\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mcased_key\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m\"connecttimeoutms\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mtimeout\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    773\u001b[0m                     )\n\u001b[0;32m--> 774\u001b[0;31m                 res = uri_parser.parse_uri(\n\u001b[0m\u001b[1;32m    775\u001b[0m                     \u001b[0mentity\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    776\u001b[0m                     \u001b[0mport\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.12/dist-packages/pymongo/uri_parser.py\u001b[0m in \u001b[0;36mparse_uri\u001b[0;34m(uri, default_port, validate, warn, normalize, connect_timeout, srv_service_name, srv_max_hosts)\u001b[0m\n\u001b[1;32m    540\u001b[0m         \u001b[0mconnect_timeout\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mconnect_timeout\u001b[0m \u001b[0;32mor\u001b[0m \u001b[0moptions\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mget\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m\"connectTimeoutMS\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    541\u001b[0m         \u001b[0mdns_resolver\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0m_SrvResolver\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mfqdn\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mconnect_timeout\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0msrv_service_name\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0msrv_max_hosts\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 542\u001b[0;31m         \u001b[0mnodes\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mdns_resolver\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mget_hosts\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    543\u001b[0m         \u001b[0mdns_options\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mdns_resolver\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mget_options\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    544\u001b[0m         \u001b[0;32mif\u001b[0m \u001b[0mdns_options\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.12/dist-packages/pymongo/srv_resolver.py\u001b[0m in \u001b[0;36mget_hosts\u001b[0;34m(self)\u001b[0m\n\u001b[1;32m    138\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    139\u001b[0m     \u001b[0;32mdef\u001b[0m \u001b[0mget_hosts\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m)\u001b[0m \u001b[0;34m->\u001b[0m \u001b[0mlist\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0mtuple\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0mstr\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mAny\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 140\u001b[0;31m         \u001b[0m_\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mnodes\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0m_get_srv_response_and_hosts\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;32mTrue\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    141\u001b[0m         \u001b[0;32mreturn\u001b[0m \u001b[0mnodes\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    142\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.12/dist-packages/pymongo/srv_resolver.py\u001b[0m in \u001b[0;36m_get_srv_response_and_hosts\u001b[0;34m(self, encapsulate_errors)\u001b[0m\n\u001b[1;32m    118\u001b[0m         \u001b[0mself\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mencapsulate_errors\u001b[0m\u001b[0;34m:\u001b[0m \u001b[0mbool\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    119\u001b[0m     ) -> tuple[resolver.Answer, list[tuple[str, Any]]]:\n\u001b[0;32m--> 120\u001b[0;31m         \u001b[0mresults\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0m_resolve_uri\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mencapsulate_errors\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    121\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    122\u001b[0m         \u001b[0;31m# Construct address tuples\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.12/dist-packages/pymongo/srv_resolver.py\u001b[0m in \u001b[0;36m_resolve_uri\u001b[0;34m(self, encapsulate_errors)\u001b[0m\n\u001b[1;32m    112\u001b[0m                 \u001b[0;32mraise\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    113\u001b[0m             \u001b[0;31m# Else, raise all errors as ConfigurationError.\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 114\u001b[0;31m             \u001b[0;32mraise\u001b[0m \u001b[0mConfigurationError\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mstr\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mexc\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m)\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0;32mNone\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    115\u001b[0m         \u001b[0;32mreturn\u001b[0m \u001b[0mresults\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    116\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mConfigurationError\u001b[0m: The DNS query name does not exist: _mongodb._tcp.cluster0.mongodb.net."
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# ===============================\n",
        "# 🎯 Employee Dashboard with MongoDB\n",
        "# ===============================\n",
        "\n",
        "import streamlit as st\n",
        "from pymongo import MongoClient\n",
        "import pandas as pd\n",
        "\n",
        "# -----------------------------\n",
        "# ⚙️ Page Config\n",
        "# -----------------------------\n",
        "st.set_page_config(\n",
        "    page_title=\"Employee Dashboard\",\n",
        "    layout=\"wide\"\n",
        ")\n",
        "\n",
        "st.title(\"👨‍💼 Employee Salary & Job Role Dashboard\")\n",
        "\n",
        "# -----------------------------\n",
        "# 🔐 MongoDB Connection\n",
        "# -----------------------------\n",
        "try:\n",
        "    client = MongoClient(st.secrets[\"mongodb\"][\"uri\"])\n",
        "    db = client[\"employee_db\"]         # Database name\n",
        "    collection = db[\"employees\"]       # Collection name\n",
        "    st.success(\"✅ Connected to MongoDB successfully!\")\n",
        "except Exception as e:\n",
        "    st.error(f\"❌ Connection Error: {e}\")\n",
        "\n",
        "# -----------------------------\n",
        "# 📥 Add Employee Form\n",
        "# -----------------------------\n",
        "st.subheader(\"➕ Add New Employee\")\n",
        "\n",
        "with st.form(\"employee_form\"):\n",
        "    emp_id = st.text_input(\"Employee ID\")\n",
        "    emp_name = st.text_input(\"Employee Name\")\n",
        "    job_role = st.text_input(\"Job Role\")\n",
        "    salary = st.number_input(\"Salary\", min_value=0)\n",
        "    submitted = st.form_submit_button(\"Add Employee\")\n",
        "\n",
        "    if submitted:\n",
        "        if emp_id and emp_name and job_role:\n",
        "            doc = {\n",
        "                \"EMPLOYEE_ID\": emp_id,\n",
        "                \"NAME\": emp_name,\n",
        "                \"JOB_ROLE\": job_role,\n",
        "                \"SALARY\": salary\n",
        "            }\n",
        "            collection.insert_one(doc)\n",
        "            st.success(f\"✅ Employee {emp_name} added successfully!\")\n",
        "        else:\n",
        "            st.warning(\"⚠️ Please fill all fields before submitting.\")\n",
        "\n",
        "# -----------------------------\n",
        "# 📊 Display Employee Data\n",
        "# -----------------------------\n",
        "st.subheader(\"📋 Employee Records\")\n",
        "\n",
        "data = list(collection.find({}, {\"_id\": 0}))  # Hide MongoDB’s internal _id field\n",
        "if data:\n",
        "    df = pd.DataFrame(data)\n",
        "    st.dataframe(df, use_container_width=True)\n",
        "else:\n",
        "    st.info(\"No records found. Add some employees above!\")\n",
        "\n",
        "# -----------------------------\n",
        "# ❌ Delete Employee\n",
        "# -----------------------------\n",
        "st.subheader(\"🗑️ Delete Employee\")\n",
        "\n",
        "del_id = st.text_input(\"Enter Employee ID to delete\")\n",
        "if st.button(\"Delete\"):\n",
        "    result = collection.delete_one({\"EMPLOYEE_ID\": del_id})\n",
        "    if result.deleted_count > 0:\n",
        "        st.success(f\"✅ Employee ID {del_id} deleted successfully!\")\n",
        "    else:\n",
        "        st.warning(f\"⚠️ Employee ID {del_id} not found.\")\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "G5HJp5XYk6lO",
        "outputId": "a5a2b8d7-c645-4827-e90f-8e3593311947"
      },
      "execution_count": 11,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "2025-11-13 05:04:25.781 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.782 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.785 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.787 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.801 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.802 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.803 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.804 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.805 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.806 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.808 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.809 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.810 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.811 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.812 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.813 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.813 Session state does not function when running a script without `streamlit run`\n",
            "2025-11-13 05:04:25.814 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.815 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.817 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.817 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.818 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.819 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.820 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.822 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.823 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.824 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.824 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.825 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.826 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.826 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.827 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.828 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.829 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.831 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.831 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.832 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.833 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.834 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.835 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.836 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.836 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.838 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.839 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.839 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.840 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.840 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.842 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.843 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:25.844 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:26.084 Please replace `use_container_width` with `width`.\n",
            "\n",
            "`use_container_width` will be removed after 2025-12-31.\n",
            "\n",
            "For `use_container_width=True`, use `width='stretch'`. For `use_container_width=False`, use `width='content'`.\n",
            "2025-11-13 05:04:26.137 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:26.138 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:26.139 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:26.140 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:26.141 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:26.142 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:26.143 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:26.144 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:26.145 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:26.146 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:26.147 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:26.148 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:26.149 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:26.151 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:26.153 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:26.154 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:26.156 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:26.157 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-11-13 05:04:26.158 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!streamlit run app.py --server.port 8501 --server.headless true\n",
        "|"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 108
        },
        "id": "Q_fvwnlamfts",
        "outputId": "83cf90bc-1d93-4d08-9378-b50c62614c5c"
      },
      "execution_count": 12,
      "outputs": [
        {
          "output_type": "error",
          "ename": "SyntaxError",
          "evalue": "invalid syntax (ipython-input-3389025387.py, line 2)",
          "traceback": [
            "\u001b[0;36m  File \u001b[0;32m\"/tmp/ipython-input-3389025387.py\"\u001b[0;36m, line \u001b[0;32m2\u001b[0m\n\u001b[0;31m    |\u001b[0m\n\u001b[0m    ^\u001b[0m\n\u001b[0;31mSyntaxError\u001b[0m\u001b[0;31m:\u001b[0m invalid syntax\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!streamlit run app.py --server.port 8501 --server.headless true\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "rKVSh1gmmgOP",
        "outputId": "e785db48-1eb1-48f0-e263-aacb6dfa3d61"
      },
      "execution_count": 14,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Usage: streamlit run [OPTIONS] [TARGET] [ARGS]...\n",
            "Try 'streamlit run --help' for help.\n",
            "\n",
            "Error: Invalid value: File does not exist: app.py\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!streamlit run app1.py --server.port 8501 --server.headless true\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "W9-XT80Xmmo5",
        "outputId": "f10ff80d-4e3a-4dc6-cb49-4b52bda93673"
      },
      "execution_count": 15,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Usage: streamlit run [OPTIONS] [TARGET] [ARGS]...\n",
            "Try 'streamlit run --help' for help.\n",
            "\n",
            "Error: Invalid value: File does not exist: app1.py\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "%%writefile app.py\n",
        "import streamlit as st\n",
        "from pymongo import MongoClient\n",
        "import pandas as pd\n",
        "\n",
        "st.set_page_config(page_title=\"Employee Dashboard\", layout=\"wide\")\n",
        "st.title(\"👨‍💼 Employee Salary & Job Role Dashboard\")\n",
        "\n",
        "# --- MongoDB Connection ---\n",
        "try:\n",
        "    client = MongoClient(st.secrets[\"mongodb\"][\"uri\"])\n",
        "    db = client[\"employee_db\"]\n",
        "    collection = db[\"employees\"]\n",
        "    st.success(\"✅ Connected to MongoDB successfully!\")\n",
        "except Exception as e:\n",
        "    st.error(f\"❌ Connection Error: {e}\")\n",
        "\n",
        "# --- Add Employee Form ---\n",
        "st.subheader(\"➕ Add New Employee\")\n",
        "with st.form(\"employee_form\"):\n",
        "    emp_id = st.text_input(\"Employee ID\")\n",
        "    emp_name = st.text_input(\"Employee Name\")\n",
        "    job_role = st.text_input(\"Job Role\")\n",
        "    salary = st.number_input(\"Salary\", min_value=0)\n",
        "    submitted = st.form_submit_button(\"Add Employee\")\n",
        "    if submitted:\n",
        "        if emp_id and emp_name and job_role:\n",
        "            d\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "N-vV2MGsmwkv",
        "outputId": "b59785a2-fae1-40b8-f8cf-1855584829b5"
      },
      "execution_count": 16,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Writing app.py\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!streamlit run app.py --server.port 8501 --server.headless true\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "T7nIJdimmyJz",
        "outputId": "b2f700e9-4434-4457-efef-57885b1d4d14"
      },
      "execution_count": 17,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\n",
            "Collecting usage statistics. To deactivate, set browser.gatherUsageStats to false.\n",
            "\u001b[0m\n",
            "\u001b[0m\n",
            "\u001b[34m\u001b[1m  You can now view your Streamlit app in your browser.\u001b[0m\n",
            "\u001b[0m\n",
            "\u001b[34m  Local URL: \u001b[0m\u001b[1mhttp://localhost:8501\u001b[0m\n",
            "\u001b[34m  Network URL: \u001b[0m\u001b[1mhttp://172.28.0.12:8501\u001b[0m\n",
            "\u001b[34m  External URL: \u001b[0m\u001b[1mhttp://34.83.105.229:8501\u001b[0m\n",
            "\u001b[0m\n",
            "\u001b[34m  Stopping...\u001b[0m\n",
            "\u001b[34m  Stopping...\u001b[0m\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install pyngrok\n",
        "\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "iE_7LMr5nURj",
        "outputId": "f1836a0b-160d-40c3-c7a8-85a96f72efaa"
      },
      "execution_count": 18,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Collecting pyngrok\n",
            "  Downloading pyngrok-7.4.1-py3-none-any.whl.metadata (8.1 kB)\n",
            "Requirement already satisfied: PyYAML>=5.1 in /usr/local/lib/python3.12/dist-packages (from pyngrok) (6.0.3)\n",
            "Downloading pyngrok-7.4.1-py3-none-any.whl (25 kB)\n",
            "Installing collected packages: pyngrok\n",
            "Successfully installed pyngrok-7.4.1\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "from pyngrok import ngrok\n",
        "public_url = ngrok.connect(8501)\n",
        "print(\"Public URL →\", public_url)\n",
        "\n",
        "!streamlit run app.py --server.port 8501 --server.headless true &\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 474
        },
        "id": "LpNm5W9XnVER",
        "outputId": "ace5e242-b529-453e-d3ef-0d0d185e2b81"
      },
      "execution_count": 19,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": []
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "ERROR:pyngrok.process.ngrok:t=2025-11-13T05:09:11+0000 lvl=eror msg=\"failed to reconnect session\" obj=tunnels.session err=\"authentication failed: Usage of ngrok requires a verified account and authtoken.\\n\\nSign up for an account: https://dashboard.ngrok.com/signup\\nInstall your authtoken: https://dashboard.ngrok.com/get-started/your-authtoken\\r\\n\\r\\nERR_NGROK_4018\\r\\n\"\n",
            "ERROR:pyngrok.process.ngrok:t=2025-11-13T05:09:11+0000 lvl=eror msg=\"session closing\" obj=tunnels.session err=\"authentication failed: Usage of ngrok requires a verified account and authtoken.\\n\\nSign up for an account: https://dashboard.ngrok.com/signup\\nInstall your authtoken: https://dashboard.ngrok.com/get-started/your-authtoken\\r\\n\\r\\nERR_NGROK_4018\\r\\n\"\n",
            "ERROR:pyngrok.process.ngrok:t=2025-11-13T05:09:11+0000 lvl=eror msg=\"terminating with error\" obj=app err=\"authentication failed: Usage of ngrok requires a verified account and authtoken.\\n\\nSign up for an account: https://dashboard.ngrok.com/signup\\nInstall your authtoken: https://dashboard.ngrok.com/get-started/your-authtoken\\r\\n\\r\\nERR_NGROK_4018\\r\\n\"\n"
          ]
        },
        {
          "output_type": "error",
          "ename": "PyngrokNgrokError",
          "evalue": "The ngrok process errored on start: authentication failed: Usage of ngrok requires a verified account and authtoken.\\n\\nSign up for an account: https://dashboard.ngrok.com/signup\\nInstall your authtoken: https://dashboard.ngrok.com/get-started/your-authtoken\\r\\n\\r\\nERR_NGROK_4018\\r\\n.",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mPyngrokNgrokError\u001b[0m                         Traceback (most recent call last)",
            "\u001b[0;32m/tmp/ipython-input-2655276404.py\u001b[0m in \u001b[0;36m<cell line: 0>\u001b[0;34m()\u001b[0m\n\u001b[1;32m      1\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0mpyngrok\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mngrok\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 2\u001b[0;31m \u001b[0mpublic_url\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mngrok\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mconnect\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;36m8501\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      3\u001b[0m \u001b[0mprint\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m\"Public URL →\"\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mpublic_url\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      4\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      5\u001b[0m \u001b[0mget_ipython\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0msystem\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m'streamlit run app.py --server.port 8501 --server.headless true &'\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.12/dist-packages/pyngrok/ngrok.py\u001b[0m in \u001b[0;36mconnect\u001b[0;34m(addr, proto, name, pyngrok_config, **options)\u001b[0m\n\u001b[1;32m    385\u001b[0m     \u001b[0mlogger\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0minfo\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34mf\"Opening tunnel named: {name}\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    386\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 387\u001b[0;31m     \u001b[0mapi_url\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mget_ngrok_process\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mpyngrok_config\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mapi_url\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    388\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    389\u001b[0m     \u001b[0mlogger\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mdebug\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34mf\"Creating tunnel with options: {options}\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.12/dist-packages/pyngrok/ngrok.py\u001b[0m in \u001b[0;36mget_ngrok_process\u001b[0;34m(pyngrok_config)\u001b[0m\n\u001b[1;32m    201\u001b[0m     \u001b[0minstall_ngrok\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mpyngrok_config\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    202\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 203\u001b[0;31m     \u001b[0;32mreturn\u001b[0m \u001b[0mprocess\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mget_process\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mpyngrok_config\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    204\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    205\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.12/dist-packages/pyngrok/process.py\u001b[0m in \u001b[0;36mget_process\u001b[0;34m(pyngrok_config)\u001b[0m\n\u001b[1;32m    269\u001b[0m         \u001b[0;32mreturn\u001b[0m \u001b[0m_current_processes\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0mpyngrok_config\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mngrok_path\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    270\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 271\u001b[0;31m     \u001b[0;32mreturn\u001b[0m \u001b[0m_start_process\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mpyngrok_config\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    272\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    273\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.12/dist-packages/pyngrok/process.py\u001b[0m in \u001b[0;36m_start_process\u001b[0;34m(pyngrok_config)\u001b[0m\n\u001b[1;32m    445\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    446\u001b[0m         \u001b[0;32mif\u001b[0m \u001b[0mngrok_process\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mstartup_error\u001b[0m \u001b[0;32mis\u001b[0m \u001b[0;32mnot\u001b[0m \u001b[0;32mNone\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 447\u001b[0;31m             raise PyngrokNgrokError(f\"The ngrok process errored on start: {ngrok_process.startup_error}.\",\n\u001b[0m\u001b[1;32m    448\u001b[0m                                     \u001b[0mngrok_process\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mlogs\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    449\u001b[0m                                     ngrok_process.startup_error)\n",
            "\u001b[0;31mPyngrokNgrokError\u001b[0m: The ngrok process errored on start: authentication failed: Usage of ngrok requires a verified account and authtoken.\\n\\nSign up for an account: https://dashboard.ngrok.com/signup\\nInstall your authtoken: https://dashboard.ngrok.com/get-started/your-authtoken\\r\\n\\r\\nERR_NGROK_4018\\r\\n."
          ]
        }
      ]
    }
  ],
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyMk/zX1yuVCp2GUlVSBEVfw",
      "include_colab_link": True
    },
    "kernelspec": {
      "display_name": "Python 3",
      "name": "python3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 0
}
