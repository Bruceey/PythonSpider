ajax = function (t, n) {

    "object" == typeof t && (n = t,
        t = void 0),
        n = n || {};
    var r, i, o, a, s, u, l, c, f = d.ajaxSetup({}, n), p = f.context || f,
        h = f.context && (p.nodeType || p.jquery) ? d(p) : d.event, g = d.Deferred(), m = d.Callbacks("once memory"),
        v = f.statusCode || {}, y = {}, x = {}, b = 0, w = "canceled",
        T = {
            readyState: 0,
            getResponseHeader: function (e) {
                var t;
                if (2 === b) {
                    if (!c)
                        for (c = {}; t = Dt.exec(a);)
                            c[t[1].toLowerCase()] = t[2];
                    t = c[e.toLowerCase()]
                }
                return null == t ? null : t
            },
            getAllResponseHeaders: function () {
                return 2 === b ? a : null
            },
            setRequestHeader: function (e, t) {
                var n = e.toLowerCase();
                return b || (e = x[n] = x[n] || e,
                    y[e] = t),
                    this
            },
            overrideMimeType: function (e) {
                return b || (f.mimeType = e),
                    this
            },
            statusCode: function (e) {
                var t;
                if (e)
                    if (b < 2)
                        for (t in e)
                            v[t] = [v[t], e[t]];
                    else
                        T.always(e[T.status]);
                return this
            },
            abort: function (e) {
                var t = e || w;
                return l && l.abort(t),
                    C(0, t),
                    this
            }
        };
    if (g.promise(T).complete = m.add,
        T.success = T.done,
        T.error = T.fail,
        f.url = ((t || f.url || Mt) + "").replace(St, "").replace(Lt, Ot[1] + "//"),
        f.type = n.method || n.type || f.method || f.type,
        f.dataTypes = d.trim(f.dataType || "*").toLowerCase().match(j) || [""],
    null == f.crossDomain && (r = Ht.exec(f.url.toLowerCase()),
        f.crossDomain = !(!r || r[1] === Ot[1] && r[2] === Ot[2] && (r[3] || ("http:" === r[1] ? "80" : "443")) === (Ot[3] || ("http:" === Ot[1] ? "80" : "443")))),
    f.data && f.processData && "string" != typeof f.data && (f.data = d.param(f.data, f.traditional)),
        Pt(qt, f, n, T),
    2 === b)
        return T;
    (u = d.event && f.global) && 0 == d.active++ && d.event.trigger("ajaxStart"),
        f.type = f.type.toUpperCase(),
        f.hasContent = !jt.test(f.type),
        o = f.url,
    f.hasContent || (f.data && (o = f.url += (Nt.test(o) ? "&" : "?") + f.data,
        delete f.data),
    !1 === f.cache && (f.url = At.test(o) ? o.replace(At, "$1_=" + Et++) : o + (Nt.test(o) ? "&" : "?") + "_=" + Et++)),
    f.ifModified && (d.lastModified[o] && T.setRequestHeader("If-Modified-Since", d.lastModified[o]),
    d.etag[o] && T.setRequestHeader("If-None-Match", d.etag[o])),
    (f.data && f.hasContent && !1 !== f.contentType || n.contentType) && T.setRequestHeader("Content-Type", f.contentType),
        T.setRequestHeader("Accept", f.dataTypes[0] && f.accepts[f.dataTypes[0]] ? f.accepts[f.dataTypes[0]] + ("*" !== f.dataTypes[0] ? ", " + Ft + "; q=0.01" : "") : f.accepts["*"]);
    return f.url
}