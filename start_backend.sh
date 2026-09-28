#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export PATH="$PWD/.toolchain/node/bin:$PATH"
cd backend
exec npm run dev
