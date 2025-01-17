import types
import traceback

from ..parameters import ORG, RELATIVE, OMAP
from ..fabric import Fabric
from ..lib import readSets
from ..core.helpers import console, mergeDict
from ..core.files import (
    normpath,
    abspath,
    APIREF,
    APP_CODE,
    APP_APP,
    TEMP_DIR,
    expanduser as ex,
    setDir,
    prefixSlash,
    splitPath,
    isDir,
    getLocation,
    backendRep,
)
from ..core.timestamp import SILENT_D, AUTO, DEEP, TERSE, VERBOSE, silentConvert
from .find import findAppConfig, findAppClass
from .helpers import getText, runsInNotebook, dm, dh
from .settings import setAppSpecs, setAppSpecsApi
from .zipdata import zipApi
from .volumes import volumesApi
from .interchange import interchangeApi
from .links import linksApi, outLink
from .text import textApi
from .sections import sectionsApi
from .display import displayApi
from .search import searchApi
from .data import getModulesData
from .repo import checkoutRepo


# SET UP A TF API FOR AN APP


FROM_TF_METHODS = """
    banner
    silentOn
    silentOff
    isSilent
    setSilent
    info
    warning
    error
    indent
    featuresOnly
""".strip().split()


class App:
    def __init__(
        self,
        cfg,
        appName,
        appPath,
        commit,
        release,
        local,
        backend,
        _browse,
        hoist=False,
        version=None,
        checkout="",
        mod=[],
        locations=None,
        modules=None,
        volume=None,
        collection=None,
        api=None,
        setFile="",
        silent=SILENT_D,
        loadData=True,
        _withGc=True,
        **configOverrides,
    ):
        """Set up the advanced TF API.

        The parameters are explained in `tf.about.usefunc`.

        Parameters
        ----------
        appName, appPath, checkout, version: string
        commit, release, local: string
        backend: string
        checkout: string, optional ""
        mod: string or iterable, optional []
        version: string, optional None
        locations, modules: string, optional None
        collection, volume: string, optional None
        api: object, optional, `None`
        setFile: string, optional, `None`
        silent: string, optional tf.core.timestamp.SILENT_D
            See `tf.core.timestamp.Timestamp`
        hoist: dict, optional False
        configOverrides: key value pairs

        _withGc: boolean, optional True
            If False, it disables the Python garbage collector before
            loading features. Used to experiment with performance.
        """

        silent = silentConvert(silent)

        self.context = None
        """Result of interpreting all configuration options in `config.yaml`.

        See Also
        --------
        tf.advanced.settings.showContext
        """

        self.inNb = runsInNotebook()

        mergeDict(cfg, configOverrides)

        for (key, value) in dict(
            isCompatible=cfg.get("isCompatible", None),
            backend=backend,
            appName=appName,
            api=api,
            version=version,
            volume=volume,
            collection=collection,
            silent=silent,
            loadData=loadData,
            _browse=_browse,
        ).items():
            setattr(self, key, value)

        setattr(self, "dm", dm)
        setattr(self, "dh", dh)

        setAppSpecs(self, cfg)
        aContext = self.context
        version = aContext.version

        setDir(self)

        self.sets = None

        if not self.api:
            self.sets = None
            if setFile:
                sets = readSets(setFile)
                if sets:
                    self.sets = sets
                    console(f'Sets from {setFile}: {", ".join(sets)}')
            specs = getModulesData(
                self, backend, mod, locations, modules, version, checkout, silent
            )

            if specs:
                (locations, modules) = specs
                self.tempDir = f"{self.repoLocation}/{TEMP_DIR}"
                TF = Fabric(
                    locations=locations,
                    modules=modules,
                    volume=volume,
                    collection=collection,
                    silent=silent,
                    _withGc=_withGc,
                )
                self.TF = TF
                if loadData:
                    api = TF.load("", silent=silent)
                    if api:
                        self.api = api
                        excludedFeatures = aContext.excludedFeatures
                        allFeatures = TF.explore(silent=DEEP, show=True)
                        loadableFeatures = allFeatures["nodes"] + allFeatures["edges"]
                        useFeatures = [
                            f
                            for f in loadableFeatures
                            if f not in excludedFeatures and not f.startswith(OMAP)
                        ]
                        result = TF.load(useFeatures, add=True, silent=silent)
                        if result is False:
                            self.api = None
                else:
                    self.api = None
                    console(
                        """
No data has been loaded.
Most of the Text-Fabric API has not been loaded.
"""
                    )
            else:
                self.TF = None
                self.api = None

        if self.api:
            self.TF = self.api.TF

        volumesApi(self)

        if self.api:
            for m in FROM_TF_METHODS:
                setattr(self, m, getattr(self.TF, m))

            zipApi(self)
            interchangeApi(self)

            featuresOnly = self.featuresOnly

            if not featuresOnly:
                self.getText = types.MethodType(getText, self)
            linksApi(self, silent=silent)
            if not featuresOnly:
                searchApi(self)
                sectionsApi(self)
                setAppSpecsApi(self, cfg)
                displayApi(self, silent=silent)
                textApi(self)
            setattr(self, "isLoaded", self.api.isLoaded)
            if hoist:
                # docs = self.api.makeAvailableIn(hoist)
                self.api.makeAvailableIn(hoist)
                if silent in {VERBOSE, AUTO, TERSE}:
                    if self.inNb:
                        dh(
                            "<div><b>Text-Fabric API:</b> names "
                            + outLink(
                                "N F E L T S C TF",
                                APIREF,
                                title="doc",
                                asHtml=True,
                            )
                            + " directly usable</div><hr>"
                        )

            silentOff = self.silentOff
            silentOff()
        else:
            if not _browse and loadData:
                console(
                    f"""
There were problems with loading data.
The Text-Fabric API has not been loaded!
The app "{appName}" will not work!
""",
                    error=True,
                )

    def load(self, features, silent=SILENT_D):
        """Loads extra features in addition to the main dataset.

        This is the same as `tf.fabric.Fabric.load` when called with `add=True`.

        Parameters
        ----------
        features: string | iterable
            Either a string containing space separated feature names, or an
            iterable of feature names.
            The feature names are just the names of `.tf` files
            without directory information and without extension.
        silent: string, optional tf.core.timestamp.SILENT_D
            See `tf.core.timestamp.Timestamp`

        Returns
        -------
        boolean
            Whether the feature has been successfully loaded.
        """

        TF = self.TF

        silent = silentConvert(silent)
        return TF.load(features, add=True, silent=silent)

    def reinit(self):
        """TF-Apps may override this method.
        It is called by `reuse`. Hence it needs to be present.
        """

        pass

    def reuse(self, hoist=False):
        """Re-initialize the app.

        The app's settings are read again, the app's code is re-imported,
        the app's stylesheets are applied again.
        But the data is left untouched, and no time-consuming reloading of data
        takes place.

        Handy when you are developing a new app and want to experiment with it
        without the costly re-loading of the data in every cycle.

        Parameters
        ----------
        hoist: boolean, optional False
            Same as in `App`.

        !!! hint "the effect of the config settings"
            If you are developing a TF app and need to see the effects of
            the configuration settings in detail, you can conveniently
            call `reuse` and `tf.advanced.settings.showContext` in tandem.
        """

        backend = self.backend
        aContext = self.context
        appPath = aContext.appPath
        appName = aContext.appName
        local = aContext.local
        commit = aContext.commit
        release = aContext.release
        version = aContext.version
        api = self.api

        cfg = findAppConfig(
            appName,
            appPath,
            commit,
            release,
            local,
            backend,
            org=aContext.org,
            repo=aContext.repo,
            relative=prefixSlash(aContext.relative),
            version=version,
        )
        findAppClass(appName, appPath)

        setAppSpecs(self, cfg, reset=True)

        if api:
            TF = self.TF
            TF._makeApi()
            api = TF.api
            self.api = api
            self.reinit()  # may be used by custom TF apps
            linksApi(self, silent=DEEP)
            searchApi(self)
            sectionsApi(self)
            setAppSpecsApi(self, cfg)
            displayApi(self, silent=DEEP)
            textApi(self)
            if hoist:
                api.makeAvailableIn(hoist)


def findApp(
    appName,
    checkoutApp,
    dataLoc,
    backend,
    _browse,
    *args,
    silent=SILENT_D,
    version=None,
    legacy=False,
    **kwargs,
):
    """Find a TF app by name and initialize an object of its main class.

    Parameters
    ----------
    appName: string or None
        Either:

        * None, but then dataLoc should have a value
        * `app:`*path/to/tf/app*
        * *org*/*repo*
        * *org*/*repo* *relative*
        * *app*, i.e. the plain name of an official TF app
          (e.g. `bhsa`, `oldbabylonian`)

        The last case is legacy: instead of *app*, pass *org*/*repo*.

    dataLoc: string or None
        Either:

        * None, but then appName should have a value
        * path to a local directory
        * *org*/*repo*
        * *org*/*repo* *relative*

        Except for the first two cases, a trailing checkout specifier
        is allowed, like `:clone`, `:local`, `:latest`, `:hot`

        It is assumed that the location is a TF data directory;
        a vanilla app without extra configuration is initialized.

    checkoutApp: string
        The checkout specifier for the TF-app. See `tf.advanced.app.App`.

    args: mixed
        Arguments that will be passed to the initializer of the `tf.advanced.app.App`
        class.

    backend: string
        `github` or `gitlab` or a GitLab instance such as `gitlab.huc.knaw.nl`.

    kwargs: mixed
        Keyword arguments that will be passed to the initializer of the
        `tf.advanced.app.App` class.

    legacy: boolean, optional False
        If true, accept that a legacy-app is called.
        Do not give warning, and do not try to load the app in the non-legacy way.
    """

    (commit, release, local) = (None, None, None)
    extraMod = None

    appLoc = None
    if appName is not None and appName.startswith("app:"):
        appLoc = normpath(appName[4:])
    else:
        appName = normpath(appName)

    if dataLoc is None and appName is None:
        console("No TF-app and no data location specified", error=True)
        return None

    if dataLoc is not None and appName is not None:
        console("Both a TF-app and a data location are specified", error=True)
        return None

    dataOrg = None
    dataRepo = None
    dataFolder = None
    inNb = runsInNotebook()

    if silent not in {TERSE, DEEP}:
        dm("**Locating corpus resources ...**", inNb=inNb)

    if dataLoc is None:
        if appLoc:
            if ":" in appLoc:
                console(
                    "When passing an app by `app:fullpath` you cannot use :-specifiers"
                )
                return None
            appPath = ex(appLoc) if appLoc else ""
            absPath = abspath(appPath)

            if isDir(absPath):
                appDir = absPath
                appBase = ""
            else:
                console(f"{absPath} is not an existing directory", error=True)
                appBase = False
                appDir = None
            appPath = appDir
        elif "/" in appName:
            (dataOrg, rest) = appName.split("/", maxsplit=1)
            (dataRepo, *rest) = rest.split("/")
            if len(rest) > 0 and rest[-1] == APP_APP:
                appParts = rest
                dataParts = rest[0:-1] + [RELATIVE]
            elif len(rest) > 0 and rest[-1] == RELATIVE:
                appParts = rest[0:-1] + [APP_APP]
                dataParts = rest
            else:
                dataParts = rest + [RELATIVE]
                appParts = rest + [APP_APP]
            appFolder = prefixSlash("/".join(appParts))
            dataFolder = prefixSlash("/".join(dataParts))

            (commit, release, local, appBase, appDir) = checkoutRepo(
                backend,
                _browse=_browse,
                org=dataOrg,
                repo=dataRepo,
                folder=appFolder,
                checkout=checkoutApp,
                withPaths=True,
                keep=False,
                silent=silent,
                label="app",
            )
            appBaseRep = f"{appBase}/" if appBase else ""
            appPath = f"{appBaseRep}{appDir}"
        else:
            (commit, release, local, appBase, appDir) = checkoutRepo(
                backend,
                _browse=_browse,
                org=ORG,
                repo=f"app-{appName}",
                folder=APP_CODE,
                checkout=checkoutApp,
                withPaths=True,
                keep=False,
                silent=silent,
                label="app",
            )
            appBaseRep = f"{appBase}/" if appBase else ""
            appPath = f"{appBaseRep}{appDir}"
            cfg = findAppConfig(appName, appPath, commit, release, local, backend)
            provenanceSpec = kwargs.get("provenanceSpec", {})
            if provenanceSpec:
                for k in ("org", "repo", "relative"):
                    value = provenanceSpec.get(k, None)
                    if value:
                        if k == "relative":
                            value = prefixSlash(value)
                        cfg[k] = value

            dataOrg = cfg.get("provenanceSpec", {}).get("org", None)
            dataRepo = cfg.get("provenanceSpec", {}).get("repo", None)

            if not legacy:
                if dataOrg:
                    console(
                        (
                            "WARNING: in the future, pass "
                            f"`{dataOrg}/{appName}` instead of `{appName}`"
                        ),
                        error=True,
                    )
                    (commit, release, local, appBase, appDir) = checkoutRepo(
                        backend,
                        _browse=_browse,
                        org=dataOrg,
                        repo=dataRepo,
                        folder=APP_APP,
                        checkout=checkoutApp,
                        withPaths=True,
                        keep=False,
                        silent=silent,
                        label="app",
                    )
                    appBaseRep = f"{appBase}/" if appBase else ""
                    appPath = f"{appBaseRep}{appDir}"
    else:
        parts = dataLoc.split(":", maxsplit=1)
        if len(parts) == 1:
            parts.append("")
        (dataLoc, checkoutData) = parts
        if checkoutData == "":
            appPath = ex(dataLoc) if dataLoc else ""
            absPath = abspath(appPath)

            if isDir(absPath):
                (appDir, appName) = splitPath(absPath)
                appBase = ""
            else:
                console(f"{absPath} is not an existing directory", error=True)
                appBase = False
                appDir = None
            appPath = appDir
        else:
            appBase = ""
            appDir = ""
            appPath = ""
            extraMod = f"{dataLoc}:{checkoutData}"

    cfg = findAppConfig(
        appName,
        appPath,
        commit,
        release,
        local,
        backend,
        org=dataOrg,
        repo=dataRepo,
        relative=dataFolder,
        version=version,
    )
    version = cfg["provenanceSpec"].get("version", None)
    isCompatible = cfg["isCompatible"]
    if isCompatible is None:
        appClass = App
    elif not isCompatible:
        return None
    else:
        appBaseRep = f"{appBase}/" if appBase else ""
        appPath = f"{appBaseRep}{appDir}"

        appClass = findAppClass(appName, appPath) or App

    mod = kwargs.get("mod", [])
    mod = [] if mod is None else mod.split(",") if type(mod) is str else list(mod)
    if extraMod:
        if len(mod) > 0:
            mod = [extraMod, *mod]
        else:
            mod = [extraMod]
    kwargs["mod"] = mod
    try:
        app = appClass(
            cfg,
            appName,
            appPath,
            commit,
            release,
            local,
            backend,
            _browse,
            *args,
            version=version,
            silent=silent,
            **kwargs,
        )
    except Exception as e:
        if appClass is not App:
            console(
                f"There was an error loading corpus {appName}",
                error=True,
            )
            console(repr(e), error=True)
        traceback.print_exc()
        console("Text-Fabric is not loaded", error=True)
        return None
    return app


def useApp(appName, backend):
    """Make use of a corpus.

    For a detailed description, see `tf.about.usefunc`.

    Parameters
    ----------
    appName: string

    backend: string, optional None
        If present, it is `github` or `gitlab`
        or a GitLab instance such as `gitlab.huc.knaw.nl`.
        If absent, `None` or empty, it is `github`.

    args:
        Do not pass any other positional argument!

    kwargs:
        Used to initialize the corpus app that we use.
        That is either an uncustomized `tf.advanced.app.App` or
        a customization of it.

    Returns
    -------
    A: object
        The object whose attributes and methods constitute the advanced API.

    See Also
    --------
    tf.advanced.app.App
    """

    if appName.startswith("data:"):
        dataLoc = appName[5:]
        appName = None
        checkoutApp = None
    elif appName.startswith("app:"):
        dataLoc = None
        checkoutApp = None
    else:
        dataLoc = None
        parts = appName.split(":", maxsplit=1)
        if len(parts) == 1:
            parts.append("")
        (appName, checkoutApp) = parts

    backend = backendRep(backend, 'norm')

    return (appName, checkoutApp, dataLoc, backend)


def loadApp(silent=DEEP):
    """Loads a given TF app or loads the TF app based on the working directory.

    It assumes that the dataset sits in a clone from a backend (github/gitlab),
    and it will load this data.

    Parameters
    ----------
    silent: string, optional "deep"
        The level of silence in which the loading will happen.
        The default is as silent as possible.

    Returns
    -------
    app: object|void
        The handle to the loaded TF dataset, if it is successfully loaded, else `None`.
    """
    (backend, org, repo, relative) = getLocation()

    if any(s is None for s in (backend, org, repo, relative)):
        console(
            "Not working in a repo: "
            f"backend={backend} org={org} repo={repo} relative={relative}"
        )
        return None

    (appName, checkoutApp, dataLoc, backend) = useApp(f"{org}/{repo}{relative}:clone", backend)

    return findApp(appName, checkoutApp, dataLoc, backend, False, checkout="clone", silent=silent)
